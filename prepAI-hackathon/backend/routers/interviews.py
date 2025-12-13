from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import schemas, crud
from services import ai_scoring

router = APIRouter()

@router.post("/submit-answer", response_model=schemas.ScoreResponse)
def submit_answer(attempt: schemas.AnswerSubmit, db: Session = Depends(get_db)):
    # 1. Get task to find expected skill/context?
    # The scoring function in requirements takes "expected_answer". 
    # But we don't store expected answers in the DB in this simple schema.
    # The requirement says: "Implement EXACTLY ... score_answer(user_answer, expected_answer)"
    # I need to provide an expected answer.
    # I'll fake it or infer it.
    # Let's say expected answer is related to the task skill.
    
    task = crud.get_task_by_id(db, attempt.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    # Mock expected answer based on skill (for hackathon demo purpose)
    # In a real app, this would come from a question bank.
    expected_answer = f"The {task.skill} concept involves..." # Placeholder
    if task.skill == "SQL":
        expected_answer = "SELECT * FROM table WHERE condition"
    elif task.skill == "Python":
        expected_answer = "def function(): return True"
        
    # If user answer is empty, maybe handle?
    
    # 2. Score it
    scores = ai_scoring.score_answer(attempt.answer_text, expected_answer)
    
    # 3. Save Attempt
    crud.create_interview_attempt(db, attempt.task_id, attempt.answer_text, scores)
    
    # 4. Update Plan Score/Readiness?
    # We should interpret this score as the new readiness for the plan?
    # Or just record it.
    # Let's record a new Score entry for the plan.
    crud.create_score(db, task.plan_id, scores['readiness'])
    
    return schemas.ScoreResponse(**scores)
