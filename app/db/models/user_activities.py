from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class ExtendedUserActivity(Base):
    """Extended version of UserActivity with additional tracking fields"""
    __tablename__ = "extended_user_activities"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ad_id = Column(Integer, ForeignKey("ads.id"))
    activity_type = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Additional tracking fields
    session_id = Column(String, index=True)
    time_spent = Column(Float)  # Time spent in seconds
    scroll_depth = Column(Float)  # Percentage of content scrolled
    device_type = Column(String)
    referrer = Column(String)
    
    # Location data
    country = Column(String)
    city = Column(String)
    
    # Relationships
    user = relationship("User", back_populates="extended_activities")
    ad = relationship("Ad", back_populates="extended_user_interactions")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "ad_id": self.ad_id,
            "activity_type": self.activity_type,
            "timestamp": self.timestamp,
            "session_id": self.session_id,
            "time_spent": self.time_spent,
            "scroll_depth": self.scroll_depth,
            "device_type": self.device_type,
            "referrer": self.referrer,
            "country": self.country,
            "city": self.city
        }