import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.session import Base, get_db
from app.core.schemas.ads import AdCreate

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_create_ad(client):
    ad_data = {
        "title": "Test Ad",
        "description": "Test Description",
        "image_url": "http://example.com/image.jpg",
        "category": "test",
        "price": 99.99
    }
    response = client.post("/api/v1/ads/", json=ad_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == ad_data["title"]
    assert data["price"] == ad_data["price"]

def test_get_recommendations(client):
    # First create a user and some ads
    user_response = client.post("/api/v1/users/", json={
        "email": "test@example.com",
        "password": "password123"
    })
    user_id = user_response.json()["id"]
    
    # Create some test ads
    ad_data = {
        "title": "Test Ad",
        "description": "Test Description",
        "image_url": "http://example.com/image.jpg",
        "category": "test",
        "price": 99.99
    }
    client.post("/api/v1/ads/", json=ad_data)
    
    # Test recommendations endpoint
    response = client.get(f"/api/v1/ads/recommendations/{user_id}")
    assert response.status_code == 200
    recommendations = response.json()
    assert isinstance(recommendations, list)