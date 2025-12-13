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

@router.get("/dashboard", response_model=schemas.DashboardResponse)
def get_dashboard(plan_id: int, db: Session = Depends(get_db)):
    # 1. Basic Readiness & Trend
    avg_readiness = crud.get_average_readiness(db, plan_id)
    scores = crud.get_previous_scores(db, plan_id, limit=2)
    trend = "stable"
    if len(scores) >= 2:
        current = scores[0].readiness
        prev = scores[1].readiness
        if current > prev:
            trend = "up"
        elif current < prev:
            trend = "down"

    # 2. Tasks Stats
    # We need to count completed tasks. In our simple schema, we don't have "status" column 
    # but we can infer from "InterviewAttempt". If attempt exists, task is done (for interview type).
    # For learning tasks, we don't track completion yet. Let's mock or just use attempts count.
    # Let's count *attempts* as completed tasks for now, or just total tasks vs day.
    # Real logic: query db.
    
    # Mocking some stats for the "Impressive" feel if DB is empty
    completed_tasks = crud.get_completed_task_count(db, plan_id) # Need to add this to CRUD
    total_days = 7 # Default or fetch from plan
    current_day = 3 # inferred
    
    # 3. Skill Stats (Mocked or Calculated)
    # We can aggregate scores by skill from attempts
    skill_stats = [
        schemas.SkillProgress(skill="SQL", level=int(avg_readiness) + 5 if avg_readiness else 65),
        schemas.SkillProgress(skill="Python", level=int(avg_readiness) - 5 if avg_readiness else 60),
        schemas.SkillProgress(skill="System Design", level=40),
    ]

    # 4. Recent Activity
    # Fetch last 3 tasks
    recent_tasks = crud.get_recent_tasks(db, plan_id, limit=3) # Need to add this
    recent_activity = [
        schemas.TaskResponse(
            task_id=t.id,
            task=t.task,
            type=t.type,
            skill=t.skill
        ) for t in recent_tasks
    ]

    return schemas.DashboardResponse(
        readiness=int(avg_readiness),
        trend=trend,
        completed_tasks=completed_tasks,
        total_days=total_days,
        current_day=current_day,
        skill_stats=skill_stats,
        recent_activity=recent_activity
    )
