from typing import Dict, Any, Optional, Tuple
import httpx
from ..core.config import settings
import json
import hashlib
import time
from datetime import datetime, timedelta
import base64
import re
from .transactions import transaction_service

class MPesaService:
    def __init__(self):
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.environment = settings.MPESA_ENV
        self.base_url = "https://sandbox.safaricom.co.ke" if self.environment == "sandbox" else "https://api.safaricom.co.ke"
        self._access_token = None
        self._token_expiry = None
        self.shortcode = "174379"  # Sandbox shortcode
        self.passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"  # Sandbox passkey
        self.max_attempts = 3

    def validate_phone_number(self, phone_number: str) -> Tuple[bool, str]:
        """Validate phone number format."""
        if not phone_number:
            return False, "Phone number is required"
            
        # Remove any spaces or special characters
        phone_number = re.sub(r'[^0-9+]', '', phone_number)
        
        # Check if it starts with +254
        if not phone_number.startswith('+254'):
            return False, "Phone number must start with +254"
            
        # Check length (should be 13 characters: +254 + 9 digits)
        if len(phone_number) != 13:
            return False, "Phone number must be 13 characters long (+254XXXXXXXXX)"
            
        # Check if the rest are digits
        if not phone_number[4:].isdigit():
            return False, "Phone number must contain only digits after +254"
            
        return True, phone_number

    def validate_amount(self, amount: float) -> Tuple[bool, str]:
        """Validate tip amount."""
        if not amount:
            return False, "Amount is required"
            
        if not isinstance(amount, (int, float)):
            return False, "Amount must be a number"
            
        if amount < 10:
            return False, "Minimum tip amount is KES 10"
            
        if amount > 5000:
            return False, "Maximum tip amount is KES 5,000"
            
        return True, str(amount)

    async def get_access_token(self) -> str:
        """Get M-Pesa access token."""
        if self._access_token and self._token_expiry and datetime.now() < self._token_expiry:
            return self._access_token

        try:
            auth_url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
            auth = (self.consumer_key, self.consumer_secret)
            
            async with httpx.AsyncClient() as client:
                response = await client.get(auth_url, auth=auth)
                response.raise_for_status()
                
                data = response.json()
                self._access_token = data["access_token"]
                self._token_expiry = datetime.now() + timedelta(seconds=data["expires_in"])
                
                return self._access_token
        except Exception as e:
            raise Exception(f"Failed to get access token: {str(e)}")

    async def initiate_stk_push(self, phone_number: str, amount: float) -> Dict[str, Any]:
        """Initiate STK push for payment."""
        try:
            # Validate inputs
            phone_valid, phone_message = self.validate_phone_number(phone_number)
            if not phone_valid:
                raise ValueError(phone_message)
                
            amount_valid, amount_message = self.validate_amount(amount)
            if not amount_valid:
                raise ValueError(amount_message)
            
            # Create transaction record
            transaction = await transaction_service.create_transaction(phone_number, amount)
            
            # Get access token
            access_token = await self.get_access_token()
            
            # Format phone number
            formatted_phone = phone_number.replace("+", "").replace("254", "254")
            
            # Generate timestamp
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            
            # Generate password
            password = self._generate_password(timestamp)
            
            # Prepare request payload
            payload = {
                "BusinessShortCode": self.shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": int(amount),
                "PartyA": formatted_phone,
                "PartyB": self.shortcode,
                "PhoneNumber": formatted_phone,
                "CallBackURL": f"{settings.BASE_URL}/api/v1/tip/callback",
                "AccountReference": transaction["id"],
                "TransactionDesc": "Payment for AI-TRS Tip"
            }
            
            # Make request
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/mpesa/stkpush/v1/processrequest",
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()
                
                result = response.json()
                
                # Check if STK push was successful
                if result.get("ResponseCode") == "0":
                    # Update transaction with STK push details
                    await transaction_service.update_transaction(
                        transaction["id"],
                        {
                            "stk_push_id": result["CheckoutRequestID"],
                            "status": "pending",
                            "stk_push_response": result
                        }
                    )
                    
                    return {
                        "success": True,
                        "message": "Please check your phone to complete the payment",
                        "transaction_id": transaction["id"],
                        "stk_push_id": result["CheckoutRequestID"],
                        "status": "pending"
                    }
                else:
                    # Update transaction with error
                    await transaction_service.update_transaction(
                        transaction["id"],
                        {
                            "status": "failed",
                            "error": result.get("ResponseDescription", "Failed to initiate payment")
                        }
                    )
                    
                    return {
                        "success": False,
                        "message": result.get("ResponseDescription", "Failed to initiate payment"),
                        "transaction_id": transaction["id"],
                        "status": "failed"
                    }
                
        except ValueError as e:
            # Handle validation errors
            return {
                "success": False,
                "message": str(e),
                "status": "invalid_input"
            }
        except Exception as e:
            # Handle other errors
            error_message = f"Error initiating STK push: {str(e)}"
            if transaction:
                await transaction_service.update_transaction(
                    transaction["id"],
                    {
                        "status": "failed",
                        "error": error_message
                    }
                )
            return {
                "success": False,
                "message": error_message,
                "status": "error"
            }

    def _generate_password(self, timestamp: str) -> str:
        """Generate M-Pesa API password."""
        password_str = f"{self.shortcode}{self.passkey}{timestamp}"
        return base64.b64encode(password_str.encode()).decode()

    async def verify_transaction(self, transaction_id: str) -> Dict[str, Any]:
        """Verify transaction status."""
        try:
            # Get transaction details
            transaction = await transaction_service.get_transaction(transaction_id)
            if not transaction:
                return {
                    "success": False,
                    "message": "Transaction not found",
                    "status": "not_found"
                }
            
            # Check if we've exceeded max attempts
            if transaction["attempts"] >= self.max_attempts:
                return {
                    "success": False,
                    "message": "Maximum verification attempts exceeded",
                    "status": "max_attempts_exceeded"
                }
            
            # Increment attempts
            await transaction_service.increment_attempts(transaction_id)
            
            # Get access token
            access_token = await self.get_access_token()
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/mpesa/transactionstatus/v1/query",
                    params={"TransactionID": transaction_id},
                    headers=headers
                )
                response.raise_for_status()
                
                result = response.json()
                
                # Update transaction status
                if result.get("ResultCode") == 0:
                    await transaction_service.update_transaction(
                        transaction_id,
                        {
                            "status": "completed",
                            "mpesa_response": result
                        }
                    )
                    return {
                        "success": True,
                        "message": "Transaction completed successfully",
                        "status": "completed",
                        "transaction": transaction
                    }
                else:
                    await transaction_service.update_transaction(
                        transaction_id,
                        {
                            "status": "failed",
                            "error": result.get("ResultDesc", "Transaction failed")
                        }
                    )
                    return {
                        "success": False,
                        "message": result.get("ResultDesc", "Transaction failed"),
                        "status": "failed",
                        "transaction": transaction
                    }
                
        except Exception as e:
            error_message = f"Error verifying transaction: {str(e)}"
            if transaction:
                await transaction_service.update_transaction(
                    transaction_id,
                    {
                        "status": "error",
                        "error": error_message
                    }
                )
            return {
                "success": False,
                "message": error_message,
                "status": "error"
            }

mpesa_service = MPesaService() 