from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class ModelMetrics(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    timestamp: datetime

class ModelInfo(BaseModel):
    version: str
    last_trained: datetime
    total_users: int
    total_ads: int
    metrics: Optional[ModelMetrics] = None
    parameters: Dict[str, Any]

class Error(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None