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

class AdaptScheduleRequest(BaseModel):
    plan_id: int
    task_id: int
    technical_score: int

class AdaptScheduleResponse(BaseModel):
    adapted: bool
    new_tasks_day_5: List[str]

class SkillProgress(BaseModel):
    skill: str
    level: int  # 0-100

class DashboardResponse(BaseModel):
    readiness: int
    trend: str
    completed_tasks: int
    total_days: int
    current_day: int
    skill_stats: List[SkillProgress]
    recent_activity: List[TaskResponse]


