from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models.users import User
from app.db.models.ads import UserActivity
from app.core.schemas.users import UserCreate, UserPreferences
from datetime import datetime
import json
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def create_user(self, db: Session, user: UserCreate) -> User:
        hashed_password = pwd_context.hash(user.password)
        db_user = User(
            email=user.email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def get_user(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()
    
    def update_preferences(self, db: Session, user_id: int, preferences: UserPreferences) -> User:
        db_user = self.get_user(db, user_id)
        if db_user:
            db_user.preferences = json.dumps(preferences.model_dump())
            db.commit()
            db.refresh(db_user)
        return db_user
    
    def get_activity_history(self, db: Session, user_id: int) -> List[UserActivity]:
        return db.query(UserActivity).filter(
            UserActivity.user_id == user_id
        ).order_by(UserActivity.timestamp.desc()).all()
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)