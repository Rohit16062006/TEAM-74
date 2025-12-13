from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)

class JobPlan(Base):
    __tablename__ = "job_plans"
    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String(100))
    experience = Column(String(50))
    days = Column(Integer)
    skills = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    tasks = relationship("DailyTask", back_populates="plan")
    scores = relationship("Score", back_populates="plan")

class DailyTask(Base):
    __tablename__ = "daily_tasks"
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("job_plans.id"))
    day = Column(Integer)
    task = Column(Text)
    type = Column(String(50))
    skill = Column(String(50))
    
    plan = relationship("JobPlan", back_populates="tasks")
    attempts = relationship("InterviewAttempt", back_populates="task_rel")

class InterviewAttempt(Base):
    __tablename__ = "interview_attempts"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("daily_tasks.id"))
    answer_text = Column(Text)
    technical_score = Column(Float)
    behavioral_score = Column(Float)
    comm_score = Column(Float)
    readiness_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    task_rel = relationship("DailyTask", back_populates="attempts")

class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("job_plans.id"))
    readiness = Column(Float)
    recorded_at = Column(DateTime, default=datetime.utcnow)
    
    plan = relationship("JobPlan", back_populates="scores")
