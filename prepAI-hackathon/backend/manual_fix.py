from database import SessionLocal
from services import task_generator
from models import JobPlan

db = SessionLocal()
plan_id = 5

print(f"Manually generating tasks for Plan {plan_id}...")
plan = db.query(JobPlan).filter(JobPlan.id == plan_id).first()

if plan:
    print(f"Plan found. Days: {plan.days}, Skills: {plan.skills}")
    try:
        task_generator.generate_tasks_for_plan(db, plan.id, plan.days, plan.skills)
        print("Generation function called.")
    except Exception as e:
        print(f"Error: {e}")
else:
    print("Plan not found.")

db.close()
