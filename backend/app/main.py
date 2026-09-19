from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import logs, users, holidays, mom, teams
from .database import engine, Base, get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy import text

Base.metadata.create_all(bind=engine)

# Pre-populate default teams if physical tables are empty
from .database import SessionLocal
from .models import CallHealthTeam, SucceedTeam
db = SessionLocal()
try:
    if db.query(CallHealthTeam).count() == 0:
        default_teams = [
            "Blood Connect", "Prachtiz", "CHAV", "Automation", 
            "Ambulance Connect", "Audit", "CHID", "FHIR", 
            "MIRTH Connect", "Digi Yatra", "OCR", "ChatBot"
        ]
        for team_name in default_teams:
            db.add(CallHealthTeam(name=team_name, company="CallHealth"))
        db.commit()
    
    if db.query(SucceedTeam).count() == 0:
        succeed_default_teams = ["Full Stack", "AI & ML", "Cloud Architecture", "QA & Testing"]
        for team_name in succeed_default_teams:
            db.add(SucceedTeam(name=team_name, company="Succeed International"))
        db.commit()
except Exception as e:
    print(f"[!] Warning: Could not pre-populate physical teams: {e}")
finally:
    db.close()

app = FastAPI(title="Project Tracker Workspace (CallHealth & Succeed International)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://project-tracker-k3h2.onrender.com",
        "https://project-tracker-nb5j.onrender.com",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(logs.router)
app.include_router(users.router)
app.include_router(holidays.router)
app.include_router(mom.router)
app.include_router(teams.router)

@app.get("/")
def health_check():
    return {"status":"API is running securely!"}

@app.get("/keep-alive")
def keep_alive():
    return {"status": "I am awake!"}