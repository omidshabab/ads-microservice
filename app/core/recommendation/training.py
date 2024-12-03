from sqlalchemy.orm import Session
from app.db.models.ads import UserActivity, Ad
from app.db.models.users import User
from app.core.recommendation.features import FeatureExtractor
from app.core.recommendation.model import AdsRecommender
from datetime import datetime
import json
from enum import Enum

class TrainingStatus(Enum):
    IDLE = "idle"
    TRAINING = "training"
    COMPLETED = "completed"
    FAILED = "failed"

class ModelTrainer:
    def __init__(self):
        self.feature_extractor = FeatureExtractor()
        self.recommender = AdsRecommender()
        self.status = TrainingStatus.IDLE
        self.last_training = None
        self.error_message = None
    
    async def train_model(self, db: Session):
        try:
            self.status = TrainingStatus.TRAINING
            
            # Get all activities
            activities = db.query(UserActivity).all()
            
            # Extract features
            training_data = self.feature_extractor.prepare_training_data(activities)
            
            # Train the model
            if training_data:
                self.recommender.train(training_data)
                
                # Update all user embeddings
                users = db.query(User).all()
                for user in users:
                    embedding = self.recommender.get_user_embedding(user.id)
                    user.embedding = json.dumps(embedding.tolist())
                
                # Update all ad embeddings
                ads = db.query(Ad).all()
                for ad in ads:
                    embedding = self.recommender.get_item_embedding(ad.id)
                    ad.embedding = json.dumps(embedding.tolist())
                
                db.commit()
            
            self.status = TrainingStatus.COMPLETED
            self.last_training = datetime.utcnow()
            
        except Exception as e:
            self.status = TrainingStatus.FAILED
            self.error_message = str(e)
            raise
    
    def get_status(self):
        return {
            "status": self.status.value,
            "last_training": self.last_training,
            "error_message": self.error_message
        }