from typing import Dict, Any, Optional, List
import redis
from datetime import datetime, timedelta
import json
from ..core.config import settings

class TransactionService:
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL)
        self.transaction_ttl = timedelta(days=7)  # Keep transactions for 7 days

    async def create_transaction(self, phone_number: str, amount: float) -> Dict[str, Any]:
        """Create a new transaction record."""
        transaction = {
            "id": f"TXN_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "phone_number": phone_number,
            "amount": amount,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "attempts": 0,
            "last_error": None
        }
        
        # Store transaction
        self.redis_client.setex(
            f"transaction:{transaction['id']}",
            self.transaction_ttl,
            json.dumps(transaction)
        )
        
        return transaction

    async def update_transaction(self, transaction_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update transaction status and details."""
        transaction_data = self.redis_client.get(f"transaction:{transaction_id}")
        if not transaction_data:
            return None
            
        transaction = json.loads(transaction_data)
        transaction.update(updates)
        transaction["updated_at"] = datetime.now().isoformat()
        
        # Store updated transaction
        self.redis_client.setex(
            f"transaction:{transaction_id}",
            self.transaction_ttl,
            json.dumps(transaction)
        )
        
        return transaction

    async def get_transaction(self, transaction_id: str) -> Optional[Dict[str, Any]]:
        """Get transaction details."""
        transaction_data = self.redis_client.get(f"transaction:{transaction_id}")
        if not transaction_data:
            return None
            
        return json.loads(transaction_data)

    async def get_transactions_by_phone(self, phone_number: str) -> List[Dict[str, Any]]:
        """Get all transactions for a phone number."""
        transactions = []
        for key in self.redis_client.scan_iter("transaction:*"):
            transaction_data = self.redis_client.get(key)
            if transaction_data:
                transaction = json.loads(transaction_data)
                if transaction["phone_number"] == phone_number:
                    transactions.append(transaction)
        
        return sorted(transactions, key=lambda x: x["created_at"], reverse=True)

    async def increment_attempts(self, transaction_id: str, error: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Increment transaction attempts and update error message."""
        transaction_data = self.redis_client.get(f"transaction:{transaction_id}")
        if not transaction_data:
            return None
            
        transaction = json.loads(transaction_data)
        transaction["attempts"] += 1
        transaction["last_error"] = error
        transaction["updated_at"] = datetime.now().isoformat()
        
        # Store updated transaction
        self.redis_client.setex(
            f"transaction:{transaction_id}",
            self.transaction_ttl,
            json.dumps(transaction)
        )
        
        return transaction

transaction_service = TransactionService() 