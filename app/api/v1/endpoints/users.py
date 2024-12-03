from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.services.user_service import UserService
from app.core.schemas.users import UserCreate, UserResponse, UserPreferences

router = APIRouter()
user_service = UserService()

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_service.create_user(db=db, user=user)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}/preferences")
def update_preferences(
    user_id: int,
    preferences: UserPreferences,
    db: Session = Depends(get_db)
):
    return user_service.update_preferences(db, user_id, preferences)

@router.get("/{user_id}/activity-history")
def get_user_activity(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_activity_history(db, user_id)