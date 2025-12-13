from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import schemas, crud

router = APIRouter()

@router.get("/readiness", response_model=schemas.ReadinessResponse)
def get_readiness_status(plan_id: int, db: Session = Depends(get_db)):
    # 1. Get average readiness
    avg_readiness = crud.get_average_readiness(db, plan_id)
    
    # 2. Determine Trend
    # Get last few scores
    scores = crud.get_previous_scores(db, plan_id, limit=2)
    trend = "stable"
    if len(scores) >= 2:
        current = scores[0].readiness
        prev = scores[1].readiness
        if current > prev:
            trend = "up"
        elif current < prev:
            trend = "down"
            
    return schemas.ReadinessResponse(
        readiness=int(avg_readiness),
        trend=trend
    )
