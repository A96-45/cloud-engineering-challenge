"""
Payment REST API Endpoints
This file is not yet committed - simulating WIP
"""

# In progress changes below:
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/payments', methods=['POST'])
def create_payment():
    """Create a new payment - INCOMPLETE"""
    # This endpoint is still being developed
    # Need to add:
    # - Request validation
    # - Payment processing
    # - Error handling
    pass
