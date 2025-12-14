from database import SessionLocal, engine
from models import JobPlan, DailyTask
from sqlalchemy import text

db = SessionLocal()

plan_id = 5

print(f"--- Checking Plan {plan_id} ---")
plan = db.query(JobPlan).filter(JobPlan.id == plan_id).first()

if not plan:
    print("Plan NOT FOUND")
else:
    print(f"Plan Found: {plan.job_title}, Days: {plan.days}")
    print(f"Skills ({type(plan.skills)}): {plan.skills}")
    
    tasks = db.query(DailyTask).filter(DailyTask.plan_id == plan_id).all()
    print(f"Task Count: {len(tasks)}")
    for t in tasks:
        print(f" - Day {t.day}: {t.task} ({t.skill})")

db.close()
