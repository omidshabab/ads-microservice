from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import ads, users, training
from app.config import settings
from app.db.session import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ads Recommendation Service",
    version="1.0.0",
    description="ML-powered advertising recommendation system"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ads.router, prefix=f"/api/{settings.API_VERSION}/ads", tags=["ads"])
app.include_router(users.router, prefix=f"/api/{settings.API_VERSION}/users", tags=["users"])
app.include_router(training.router, prefix=f"/api/{settings.API_VERSION}/training", tags=["training"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}