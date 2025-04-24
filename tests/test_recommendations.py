import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.schemas import RecommendationRequest, QueryType

client = TestClient(app)

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_recommendation_endpoint():
    """Test recommendation endpoint."""
    request_data = {
        "query": "I need a cheap phone for my mama",
        "context": None
    }
    
    response = client.post("/api/v1/recommend/recommend", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "session_id" in data
    assert "query_type" in data
    assert isinstance(data["query_type"], str)
    assert data["query_type"] in [qt.value for qt in QueryType]

def test_clarification_endpoint():
    """Test clarification endpoint."""
    request_data = {
        "query": "What's your maximum budget?",
        "context": {
            "previous_query": "I need a cheap phone for my mama"
        }
    }
    
    response = client.post(
        "/api/v1/recommend/clarify",
        json=request_data,
        params={"session_id": "test-session-123"}
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "session_id" in data
    assert "query_type" in data

def test_invalid_recommendation_request():
    """Test invalid recommendation request."""
    request_data = {
        "query": "",  # Empty query
        "context": None
    }
    
    response = client.post("/api/v1/recommend/recommend", json=request_data)
    assert response.status_code == 422  # Validation error

def test_tip_endpoint():
    """Test tip initiation endpoint."""
    request_data = {
        "phone_number": "+254759325915",
        "amount": 100
    }
    
    response = client.post("/api/v1/tip/initiate", json=request_data)
    assert response.status_code in [200, 400]  # 400 if M-Pesa credentials not configured
    
    if response.status_code == 200:
        data = response.json()
        assert "transaction_id" in data
        assert "status" in data
        assert "message" in data 