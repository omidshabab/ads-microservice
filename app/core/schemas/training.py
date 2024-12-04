from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.core.recommendation.training import TrainingStatus

class TrainingResponse(BaseModel):
    status: str
    timestamp: datetime
    message: Optional[str] = None