from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.recommendation.training import ModelTrainer
from app.core.recommendation.training import TrainingStatus, TrainingResponse
from datetime import datetime

router = APIRouter()
model_trainer = ModelTrainer()

@router.post("/trigger", response_model=TrainingResponse)
async def trigger_training(
    background_tasks: BackgroundTasks,
    force: bool = False,
    db: Session = Depends(get_db)
):
    # Add training task to background tasks
    background_tasks.add_task(model_trainer.train_model, db)
    
    return TrainingResponse(
        status=TrainingStatus.SCHEDULED,
        timestamp=datetime.utcnow(),
        message="Model training has been scheduled"
    )

@router.get("/status", response_model=TrainingResponse)
async def get_training_status(db: Session = Depends(get_db)):
    status = model_trainer.get_status()
    return status