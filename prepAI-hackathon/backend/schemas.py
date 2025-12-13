from pydantic import BaseModel
from typing import List, Optional

class PlanCreate(BaseModel):
    job_title: str
    experience: str
    days: int

class PlanResponse(BaseModel):
    plan_id: int
    skills: List[str]
    days: int

class TaskResponse(BaseModel):
    task_id: int
    task: str
    type: str
    skill: str

class AnswerSubmit(BaseModel):
    task_id: int
    answer_text: str

class ScoreResponse(BaseModel):
    technical: int
    behavioral: int
    comm: int
    readiness: int

class ReadinessResponse(BaseModel):
    readiness: int
    trend: str
