from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    API_VERSION: str = "v1"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str
    DB_MAX_CONNECTIONS: int = 20
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # ML Model
    MODEL_UPDATE_INTERVAL: int = 3600
    MINIMUM_TRAINING_SAMPLES: int = 100
    EMBEDDING_SIZE: int = 64
    LEARNING_RATE: float = 0.001
    
    # Recommendation
    MAX_RECOMMENDATIONS: int = 10
    SIMILARITY_THRESHOLD: float = 0.5

    class Config:
        env_file = ".env"

settings = Settings()