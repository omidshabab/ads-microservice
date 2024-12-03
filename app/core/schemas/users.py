from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime

class UserPreferences(BaseModel):
    categories: list[str] = []
    price_range: Dict[str, float] = {"min": 0, "max": float('inf')}
    custom_preferences: Dict[str, Any] = {}

class UserBase(BaseModel):
    email: EmailStr
    preferences: Optional[UserPreferences] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserActivity(BaseModel):
    user_id: int
    ad_id: int
    activity_type: str
    timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True