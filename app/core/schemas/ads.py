from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class AdBase(BaseModel):
    title: str
    description: str
    image_url: str
    category: str
    price: float

class AdCreate(AdBase):
    pass

class AdResponse(AdBase):
    id: int
    created_at: datetime
    updated_at: datetime
    similarity_score: Optional[float] = None

    class Config:
        from_attributes = True

class RecommendationResponse(BaseModel):
    ad: AdResponse
    score: float

class UserActivityBase(BaseModel):
    user_id: int
    ad_id: int
    activity_type: str  # view, click, save, purchase

class UserActivityCreate(UserActivityBase):
    pass

class UserActivityResponse(UserActivityBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True