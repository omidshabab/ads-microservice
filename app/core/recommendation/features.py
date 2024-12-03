from typing import List, Tuple
from app.db.models.ads import UserActivity
import numpy as np
from datetime import datetime, timedelta

class FeatureExtractor:
    def __init__(self):
        self.activity_weights = {
            "view": 0.2,
            "click": 0.5,
            "save": 0.8,
            "purchase": 1.0
        }
        
    def prepare_training_data(self, activities: List[UserActivity]) -> List[Tuple[int, int, float]]:
        """Convert user activities to training data with time decay."""
        training_data = []
        current_time = datetime.utcnow()
        
        for activity in activities:
            # Calculate time decay (exponential decay over 30 days)
            days_diff = (current_time - activity.timestamp).days
            time_decay = np.exp(-days_diff / 30)  # 30 days half-life
            
            # Calculate final weight
            base_weight = self.activity_weights.get(activity.activity_type, 0.1)
            final_weight = base_weight * time_decay
            
            training_data.append((
                activity.user_id,
                activity.ad_id,
                final_weight
            ))
        
        return training_data
    
    def extract_user_features(self, activities: List[UserActivity]) -> np.ndarray:
        """Extract user features based on their activity patterns."""
        features = {
            "view_count": 0,
            "click_count": 0,
            "save_count": 0,
            "purchase_count": 0,
            "total_spent": 0.0,
            "activity_frequency": 0.0
        }
        
        if not activities:
            return np.zeros(len(features))
        
        # Calculate time span
        timestamps = [a.timestamp for a in activities]
        time_span = (max(timestamps) - min(timestamps)).days + 1
        
        for activity in activities:
            if activity.activity_type == "view":
                features["view_count"] += 1
            elif activity.activity_type == "click":
                features["click_count"] += 1
            elif activity.activity_type == "save":
                features["save_count"] += 1
            elif activity.activity_type == "purchase":
                features["purchase_count"] += 1
                features["total_spent"] += activity.ad.price if activity.ad else 0
        
        # Calculate activity frequency (activities per day)
        features["activity_frequency"] = len(activities) / time_span if time_span > 0 else 0
        
        return np.array(list(features.values()))