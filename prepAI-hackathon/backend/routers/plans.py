from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from database import get_db
from models import JobPlan, DailyTask
from schemas import PlanCreate, PlanResponse, TaskResponse
from services import skill_mapper, task_generator

router = APIRouter()

# -------------------------
# Create Job Plan
# -------------------------
@router.post("/create-plan", response_model=PlanResponse)
def create_plan(plan: PlanCreate, db: Session = Depends(get_db)):
    # 1. Fetch skills if not provided
    final_skills = plan.skills
    if not final_skills:
        final_skills = skill_mapper.get_skills_for_role(plan.job_title, plan.experience)
    
    # 2. Create Plan
    new_plan = JobPlan(
        job_title=plan.job_title,
        experience=plan.experience,
        days=plan.days,
        skills=final_skills
    )
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    
    # 3. Generate Daily Tasks
    task_generator.generate_tasks_for_plan(db, new_plan.id, new_plan.days, new_plan.skills)

    return new_plan


# -------------------------
# Get Daily Task (By Day)
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
        "id": task.id,
        "plan_id": plan_id,
        "day": day,
        "task": task.task,
        "type": task.type,
        "skill": task.skill
    }

# -------------------------
# Get All Tasks for Plan
# -------------------------
@router.get("/plan-tasks", response_model=List[TaskResponse])
def get_plan_tasks(plan_id: int, db: Session = Depends(get_db)):
    tasks = (
        db.query(DailyTask)
        .filter(DailyTask.plan_id == plan_id)
        .order_by(DailyTask.day)
        .all()
    )
    
    # Self-healing: If plan exists but has no tasks, generate them.
    if not tasks:
        plan = db.query(JobPlan).filter(JobPlan.id == plan_id).first()
        if plan:
            print(f"Generating missing tasks for plan {plan_id}...")
            task_generator.generate_tasks_for_plan(db, plan.id, plan.days, plan.skills)
            tasks = (
                db.query(DailyTask)
                .filter(DailyTask.plan_id == plan_id)
                .order_by(DailyTask.day)
                .all()
            )

    return tasks

# -------------------------
# Get Specific Task by ID
# -------------------------
@router.get("/task/{task_id}", response_model=TaskResponse)
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = db.query(DailyTask).filter(DailyTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
