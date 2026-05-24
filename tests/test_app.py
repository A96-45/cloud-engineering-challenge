"""
Unit tests for Cloud Cost Optimizer application
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.app import app

@pytest.fixture
def client():
    """Create test client"""
    with app.test_client() as client:
        yield client

def test_index(client):
    """Test home endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    assert response.json['status'] == 'operational'

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_get_costs(client):
    """Test cost data endpoint"""
    response = client.get('/api/costs')
    assert response.status_code == 200
    assert 'total_monthly_cost' in response.json
    assert 'services' in response.json

def test_not_found(client):
    """Test 404 error handling"""
    response = client.get('/nonexistent')
    assert response.status_code == 404

def test_response_headers(client):
    """Test response headers"""
    response = client.get('/')
    assert response.content_type == 'application/json'
