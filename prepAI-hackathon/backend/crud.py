from sqlalchemy.orm import Session
from sqlalchemy import func
import models
from datetime import datetime

def create_job_plan(db: Session, job_title: str, experience: str, days: int, skills: list):
    db_plan = models.JobPlan(
        job_title=job_title,
        experience=experience,
        days=days,
        skills=skills
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

def create_daily_task(db: Session, plan_id: int, day: int, task: str, task_type: str, skill: str):
    db_task = models.DailyTask(
        plan_id=plan_id,
        day=day,
        task=task,
        type=task_type,
        skill=skill
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_daily_tasks(db: Session, plan_id: int, day: int):
    return db.query(models.DailyTask).filter(models.DailyTask.plan_id == plan_id, models.DailyTask.day == day).all()

def get_task_by_id(db: Session, task_id: int):
    return db.query(models.DailyTask).filter(models.DailyTask.id == task_id).first()

def create_interview_attempt(db: Session, task_id: int, answer_text: str, scores: dict):
    db_attempt = models.InterviewAttempt(
        task_id=task_id,
        answer_text=answer_text,
        technical_score=scores['technical'],
        behavioral_score=scores['behavioral'],
        comm_score=scores['comm'],
        readiness_score=scores['readiness']
    )
    db.add(db_attempt)
    db.commit()
    db.refresh(db_attempt)
    return db_attempt

def create_score(db: Session, plan_id: int, readiness: float):
    db_score = models.Score(
        plan_id=plan_id,
        readiness=readiness
    )
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score

def get_latest_readiness(db: Session, plan_id: int):
    # Retrieve the most recent Score entry for the plan
    return db.query(models.Score).filter(models.Score.plan_id == plan_id).order_by(models.Score.recorded_at.desc()).first()

def get_average_readiness(db: Session, plan_id: int):
     # Calculate average readiness from attempts linked to tasks of this plan
     # This is a bit complex in ORM, might be easier to query attempts joining tasks
     result = db.query(func.avg(models.InterviewAttempt.readiness_score))\
         .join(models.DailyTask, models.InterviewAttempt.task_id == models.DailyTask.id)\
         .filter(models.DailyTask.plan_id == plan_id)\
         .scalar()
     return result if result else 0.0

def get_previous_scores(db: Session, plan_id: int, limit: int = 5):
    return db.query(models.Score).filter(models.Score.plan_id == plan_id).order_by(models.Score.recorded_at.desc()).limit(limit).all()

def get_completed_task_count(db: Session, plan_id: int):
    # Count unique tasks that have an attempt
    return db.query(models.InterviewAttempt.task_id)\
             .join(models.DailyTask, models.InterviewAttempt.task_id == models.DailyTask.id)\
             .filter(models.DailyTask.plan_id == plan_id)\
             .distinct()\
             .count()

def get_recent_tasks(db: Session, plan_id: int, limit: int = 3):
    return db.query(models.DailyTask)\
             .filter(models.DailyTask.plan_id == plan_id)\
             .order_by(models.DailyTask.day.desc(), models.DailyTask.id.desc())\
             .limit(limit)\
             .all()
