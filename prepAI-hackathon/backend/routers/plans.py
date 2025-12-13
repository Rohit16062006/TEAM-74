from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import JobPlan, DailyTask
from schemas import PlanCreate, PlanResponse

router = APIRouter()

# -------------------------
# Create Job Plan
# -------------------------
@router.post("/create-plan", response_model=PlanResponse)
def create_plan(plan: PlanCreate, db: Session = Depends(get_db)):
    new_plan = JobPlan(
        job_title=plan.job_title,
        experience=plan.experience,
        days=plan.days,
        skills=plan.skills
    )
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)

    return new_plan


# -------------------------
# Get Daily Task
# -------------------------
@router.get("/daily-task")
def get_daily_task(plan_id: int, day: int, db: Session = Depends(get_db)):
    task = (
        db.query(DailyTask)
        .filter(DailyTask.plan_id == plan_id, DailyTask.day == day)
        .first()
    )

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "plan_id": plan_id,
        "day": day,
        "task": task.task,
        "type": task.type,
        "skill": task.skill
    }
