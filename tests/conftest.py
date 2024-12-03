import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.db.session import Base, get_db
from app.db.models.users import User
from app.db.models.ads import Ad, UserActivity

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite://"  # In-memory SQLite database

@pytest.fixture(scope="function")
def engine():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def TestingSessionLocal(engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal

@pytest.fixture(scope="function")
def db(TestingSessionLocal):
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def test_user(db):
    user = User(
        email="testuser@example.com",
        hashed_password="hashed_password",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture(scope="function")
def test_ad(db):
    ad = Ad(
        title="Test Ad",
        description="Test Description",
        image_url="http://example.com/image.jpg",
        category="test",
        price=99.99
    )
    db.add(ad)
    db.commit()
    db.refresh(ad)
    return ad

@pytest.fixture(scope="function")
def test_user_activity(db, test_user, test_ad):
    activity = UserActivity(
        user_id=test_user.id,
        ad_id=test_ad.id,
        activity_type="view"
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity