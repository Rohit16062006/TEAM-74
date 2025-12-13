from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import plans, interviews, analytics

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PrepAI Hackathon Backend")

# CORS
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(plans.router, prefix="/api", tags=["Plans"])
app.include_router(interviews.router, prefix="/api", tags=["Interviews"])
app.include_router(analytics.router, prefix="/api", tags=["Analytics"])

@app.get("/")
def health_check():
    return {"status": "ok"}

# ====================
# TEST COMMANDS (Curl)
# ====================
#
# 1. Create Plan:
# curl -X POST "http://localhost:8000/api/create-plan" -H "Content-Type: application/json" -d "{\"job_title\": \"backend_developer\", \"experience\": \"fresher\", \"days\": 7}"
#
# 2. Get Daily Task:
# curl -X GET "http://localhost:8000/api/daily-task?plan_id=1&day=1"
#
# 3. Submit Answer:
# curl -X POST "http://localhost:8000/api/submit-answer" -H "Content-Type: application/json" -d "{\"task_id\": 1, \"answer_text\": \"SELECT * FROM table\"}"
#
# 4. Get Readiness:
# curl -X GET "http://localhost:8000/api/readiness?plan_id=1"
