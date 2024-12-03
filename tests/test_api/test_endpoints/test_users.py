import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.schemas.users import UserCreate, UserPreferences

def test_create_user(client):
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "preferences": {
            "categories": ["electronics", "books"],
            "price_range": {"min": 0, "max": 1000},
            "custom_preferences": {"newsletter": True}
        }
    }
    
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert "password" not in data

def test_get_user(client):
    # First create a user
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    create_response = client.post("/api/v1/users/", json=user_data)
    user_id = create_response.json()["id"]
    
    # Test getting the user
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "password" not in data

def test_update_preferences(client):
    # Create a user first
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    create_response = client.post("/api/v1/users/", json=user_data)
    user_id = create_response.json()["id"]
    
    # Update preferences
    new_preferences = {
        "categories": ["fashion", "sports"],
        "price_range": {"min": 10, "max": 500},
        "custom_preferences": {"notifications": False}
    }
    
    response = client.put(
        f"/api/v1/users/{user_id}/preferences",
        json=new_preferences
    )
    assert response.status_code == 200
    data = response.json()
    assert "preferences" in data

def test_get_activity_history(client):
    # Create a user
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    create_response = client.post("/api/v1/users/", json=user_data)
    user_id = create_response.json()["id"]
    
    # Get activity history
    response = client.get(f"/api/v1/users/{user_id}/activity-history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)