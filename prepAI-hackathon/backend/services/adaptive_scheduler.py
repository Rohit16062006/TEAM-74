from sqlalchemy.orm import Session
import crud
import models

def adapt_plan(db: Session, plan_id: int, task_id: int, score: float):
    if score >= 70:
        return {"adapted": False, "message": None}

    # Get the failing task to identify skill
    task = crud.get_task_by_id(db, task_id)
    if not task:
        return {"adapted": False, "message": None}

    skill = task.skill
    current_day = task.day
    next_day = current_day + 1
    
    # Insert extra practice on Next Day
    new_task_name = f"Remedial: {skill} Basics Refresher"
    
    crud.create_daily_task(
        db, 
        plan_id=plan_id, 
        day=next_day, 
        task=new_task_name, 
        task_type="learning", 
        skill=skill
    )
    
    return {
        "adapted": True,
        "message": f"Low score detected. Added '{new_task_name}' to Day {next_day} schedule."
    }
