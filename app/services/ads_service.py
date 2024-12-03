from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.recommendation.model import AdsRecommender
from app.db.models.ads import Ad, UserActivity
from app.core.schemas.ads import AdCreate
from datetime import datetime
import json

from app.db.models.users import User

class AdsService:
    def __init__(self):
        self.recommender = AdsRecommender()
        
    def create_ad(self, db: Session, ad: AdCreate) -> Ad:
        db_ad = Ad(**ad.dict())
        db.add(db_ad)
        db.commit()
        db.refresh(db_ad)
        return db_ad
    
    def get_recommendations(self, db: Session, user_id: int, limit: int = 10) -> List[Ad]:
        # Get user activities
        activities = db.query(UserActivity).filter(
            UserActivity.user_id == user_id
        ).all()
        
        # Prepare training data
        training_data = [
            (act.user_id, act.ad_id, self._get_activity_weight(act.activity_type))
            for act in activities
        ]
        
        # Train model if we have data
        if training_data:
            self.recommender.train(training_data)
        
        # Get all available ads
        ads = db.query(Ad).all()
        ad_ids = [ad.id for ad in ads]
        
        # Get recommendations
        recommendations = self.recommender.recommend(user_id, ad_ids, top_k=limit)
        
        # Fetch recommended ads
        recommended_ads = []
        for ad_id, score in recommendations:
            ad = db.query(Ad).filter(Ad.id == ad_id).first()
            if ad:
                setattr(ad, 'similarity_score', score)
                recommended_ads.append(ad)
                
        return recommended_ads
    
    def track_activity(self, db: Session, activity: UserActivity) -> UserActivity:
        db_activity = UserActivity(**activity.dict())
        db.add(db_activity)
        db.commit()
        db.refresh(db_activity)
        
        # Update user embedding after new activity
        self._update_user_embedding(db, activity.user_id)
        
        return db_activity
    
    def get_categories(self, db: Session) -> List[str]:
        return db.query(Ad.category).distinct().all()
    
    def _get_activity_weight(self, activity_type: str) -> float:
        """Convert activity type to numerical weight for training."""
        weights = {
            "view": 0.2,
            "click": 0.5,
            "save": 0.8,
            "purchase": 1.0
        }
        return weights.get(activity_type, 0.1)
    
    def _update_user_embedding(self, db: Session, user_id: int):
        """Update user embedding based on recent activities."""
        activities = db.query(UserActivity).filter(
            UserActivity.user_id == user_id
        ).all()
        
        if activities:
            training_data = [
                (act.user_id, act.ad_id, self._get_activity_weight(act.activity_type))
                for act in activities
            ]
            self.recommender.train(training_data)
            
            # Save updated embedding
            embedding = self.recommender.get_user_embedding(user_id)
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                user.embedding = json.dumps(embedding.tolist())
                db.commit()