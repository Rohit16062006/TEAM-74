from sqlalchemy.orm import Session
import crud
import models

def adapt_plan(db: Session, plan_id: int, task_id: int, score: int):
    new_tasks = []
    if score < 60:
        # Get the failing task to identify skill
        task = crud.get_task_by_id(db, task_id)
        if task:
            skill = task.skill
            # Insert extra practice on Day 5
            new_task_name = f"Extra {skill} Practice"
            crud.create_daily_task(
                db, 
                plan_id=plan_id, 
                day=5, 
                task=new_task_name, 
                task_type="learning", 
                skill=skill
            )
            new_tasks.append(new_task_name)
    
    return {
        "adapted": len(new_tasks) > 0,
        "new_tasks_day_5": new_tasks
    }
