from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.services.ads_service import AdsService
from app.core.schemas.ads import AdCreate, AdResponse, RecommendationResponse
from app.core.schemas.users import UserActivity

router = APIRouter()
ads_service = AdsService()

@router.post("/", response_model=AdResponse)
def create_ad(ad: AdCreate, db: Session = Depends(get_db)):
    return ads_service.create_ad(db, ad)

@router.get("/recommendations/{user_id}", response_model=List[RecommendationResponse])
def get_recommendations(
    user_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    recommendations = ads_service.get_recommendations(db, user_id, limit)
    if not recommendations:
        raise HTTPException(status_code=404, detail="No recommendations found")
    return recommendations

@router.post("/track-activity")
def track_user_activity(activity: UserActivity, db: Session = Depends(get_db)):
    return ads_service.track_activity(db, activity)

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    return ads_service.get_categories(db)