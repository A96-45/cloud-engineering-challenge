"""
Payment Processing System - WORK IN PROGRESS
This is unfinished work that gets interrupted by urgent bug
"""

class PaymentProcessor:
    def __init__(self):
        self.transactions = []
    
    def process_payment(self, user_id, amount, currency="USD"):
        """Process payment - INCOMPLETE"""
        # TODO: Add payment gateway integration
        # TODO: Add fraud detection
        # TODO: Add error handling
        pass
    
    def refund_payment(self, transaction_id):
        """Refund payment - INCOMPLETE"""
        # TODO: Validate transaction exists
        # TODO: Check refund window
        # TODO: Process refund
        pass
