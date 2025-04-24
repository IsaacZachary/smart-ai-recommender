from fastapi import APIRouter, HTTPException, Request, Depends
from typing import Dict, Any, List
from ..models.schemas import TipRequest, TipResponse
from ..services.mpesa import mpesa_service
from ..services.transactions import transaction_service
from ..core.config import settings
import json
from datetime import datetime

router = APIRouter()

@router.post("/tip/initiate", response_model=TipResponse)
async def initiate_tip(request: TipRequest):
    """
    Initiate M-Pesa STK push for tipping.
    """
    try:
        # Validate amount
        if request.amount < 10 or request.amount > 5000:
            raise HTTPException(
                status_code=400,
                detail="Tip amount must be between KES 10 and KES 5,000"
            )
        
        # Validate phone number format
        if not request.phone_number.startswith("+254") or len(request.phone_number) != 13:
            raise HTTPException(
                status_code=400,
                detail="Phone number must be in format: +254XXXXXXXXX"
            )
        
        # Initiate STK push
        response = await mpesa_service.initiate_stk_push(
            request.phone_number,
            request.amount
        )
        
        # Check for success
        if response["success"]:
            return TipResponse(
                transaction_id=response["transaction_id"],
                status=response["status"],
                message=response["message"]
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=response["message"]
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error initiating tip: {str(e)}"
        )

@router.post("/tip/callback")
async def tip_callback(request: Request):
    """
    Handle M-Pesa callback for payment status.
    """
    try:
        # Get callback data
        data = await request.json()
        
        # Verify callback signature
        if not _verify_callback_signature(data):
            raise HTTPException(
                status_code=400,
                detail="Invalid callback signature"
            )
        
        # Process callback
        result = data.get("Body", {}).get("stkCallback", {})
        transaction_id = result.get("CheckoutRequestID")
        
        if not transaction_id:
            raise HTTPException(
                status_code=400,
                detail="Missing transaction ID in callback"
            )
        
        # Update transaction status
        if result.get("ResultCode") == 0:
            # Payment successful
            await transaction_service.update_transaction(
                transaction_id,
                {
                    "status": "completed",
                    "mpesa_response": result,
                    "completed_at": datetime.now().isoformat()
                }
            )
            return {
                "status": "success",
                "message": "Payment received successfully",
                "transaction_id": transaction_id,
                "amount": result.get("Amount"),
                "phone_number": result.get("PhoneNumber")
            }
        else:
            # Payment failed
            await transaction_service.update_transaction(
                transaction_id,
                {
                    "status": "failed",
                    "error": result.get("ResultDesc", "Payment failed"),
                    "failed_at": datetime.now().isoformat()
                }
            )
            return {
                "status": "failed",
                "message": result.get("ResultDesc", "Payment failed"),
                "transaction_id": transaction_id
            }
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing callback: {str(e)}"
        )

@router.get("/tip/status/{transaction_id}")
async def get_transaction_status(transaction_id: str):
    """
    Get transaction status.
    """
    try:
        transaction = await transaction_service.get_transaction(transaction_id)
        if not transaction:
            raise HTTPException(
                status_code=404,
                detail="Transaction not found"
            )
            
        return {
            "transaction_id": transaction["id"],
            "status": transaction["status"],
            "amount": transaction["amount"],
            "phone_number": transaction["phone_number"],
            "created_at": transaction["created_at"],
            "updated_at": transaction["updated_at"],
            "error": transaction.get("error")
        }
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting transaction status: {str(e)}"
        )

@router.get("/tip/history/{phone_number}")
async def get_transaction_history(phone_number: str):
    """
    Get transaction history for a phone number.
    """
    try:
        transactions = await transaction_service.get_transactions_by_phone(phone_number)
        return {
            "phone_number": phone_number,
            "transactions": transactions
        }
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting transaction history: {str(e)}"
        )

def _verify_callback_signature(data: Dict[str, Any]) -> bool:
    """
    Verify M-Pesa callback signature.
    This is a placeholder - implement actual signature verification
    based on M-Pesa's security requirements.
    """
    # TODO: Implement proper signature verification
    return True 