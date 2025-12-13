from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import schemas, crud
from services import skill_mapper
import random

router = APIRouter()

@router.post("/create-plan", response_model=schemas.PlanResponse)
def create_plan(plan: schemas.PlanCreate, db: Session = Depends(get_db)):
    # 1. Map skills
    skills = skill_mapper.get_skills_for_role(plan.job_title, plan.experience)
    if not skills:
        # Fallback or error? User might provide unknown role.
        # Let's default to some if empty or just return empty.
        # Requirement implies we use the map.
        pass

    # 2. Create Plan in DB
    db_plan = crud.create_job_plan(db, plan.job_title, plan.experience, plan.days, skills)
    
    # 3. Generate Daily Tasks (Simple Logic)
    # Distribute skills across days
    if skills:
        for day in range(1, plan.days + 1):
            # Pick a random skill for the day
            skill = skills[(day - 1) % len(skills)]
            
            # Create a learning task
            crud.create_daily_task(
                db, 
                plan_id=db_plan.id, 
                day=day, 
                task=f"Study {skill} fundamentals", 
                task_type="learning", 
                skill=skill
            )
            
            # Create an interview task
            crud.create_daily_task(
                db, 
                plan_id=db_plan.id, 
                day=day, 
                task=f"{skill} Mock Interview", 
                task_type="interview", 
                skill=skill
            )
            
    return schemas.PlanResponse(
        plan_id=db_plan.id,
        skills=skills,
        days=plan.days
    )

@router.get("/daily-task", response_model=list[schemas.TaskResponse])
def get_daily_tasks(plan_id: int, day: int, db: Session = Depends(get_db)):
    tasks = crud.get_daily_tasks(db, plan_id, day)
    return [
        schemas.TaskResponse(
            task_id=t.id,
            task=t.task,
            type=t.type,
            skill=t.skill
        ) for t in tasks
    ]
