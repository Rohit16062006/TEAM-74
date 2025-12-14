from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# =========================
# PLAN SCHEMAS
# =========================

class PlanCreate(BaseModel):
    job_title: str
    experience: str
    days: int
    skills: Optional[List[str]] = []


class PlanResponse(BaseModel):
    id: int
    job_title: str
    experience: str
    days: int
    skills: List[str]
    created_at: datetime

    class Config:
        from_attributes = True


# =========================
# TASK SCHEMAS
# =========================

class TaskResponse(BaseModel):
    id: int
    task: str
    type: str
    skill: str
    explanation: Optional[str] = None
    explanation_alt: Optional[str] = None

    class Config:
        from_attributes = True


# =========================
# ANSWER / INTERVIEW
# =========================

class AnswerSubmit(BaseModel):
    task_id: int
    answer_text: str


class ScoreResponse(BaseModel):
    technical_score: float
    behavioral_score: float
    comm_score: float
    readiness_score: float
    feedback: Optional[str] = None


class ReadinessResponse(BaseModel):
    readiness: float
    trend: str


# =========================
# ADAPTIVE SCHEDULING
# =========================

class AdaptScheduleRequest(BaseModel):
    plan_id: int
    task_id: int
    technical_score: float


class AdaptScheduleResponse(BaseModel):
    adapted: bool
    new_tasks_day_5: List[str]


# =========================
# DASHBOARD
# =========================

class SkillProgress(BaseModel):
    skill: str
    level: int  # 0 - 100


class DashboardResponse(BaseModel):
    readiness: float
    trend: str
    completed_tasks: int
    total_days: int
    current_day: int
    skill_stats: List[SkillProgress]
    recent_activity: List[TaskResponse]
