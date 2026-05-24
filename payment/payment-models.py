"""
Payment Models - Data structures for payment processing
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Transaction:
    """Represents a payment transaction"""
    transaction_id: str
    user_id: str
    amount: float
    currency: str
    status: str  # pending, completed, failed, refunded
    created_at: datetime
    metadata: Optional[dict] = None
    # Work in progress...
