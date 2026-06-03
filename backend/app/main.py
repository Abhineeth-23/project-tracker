from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import logs, users, holidays, mom, teams
from .database import engine, Base

Base.metadata.create_all(bind=engine)

# Pre-populate default teams if teams table is empty
from .database import SessionLocal
from .models import Team
db = SessionLocal()
try:
    if db.query(Team).count() == 0:
        default_teams = ["Digi Yatra", "OCR", "FHIR", "MIRTH Connect", "ChatBot", "Blood Connect"]
        for team_name in default_teams:
            db.add(Team(name=team_name))
        db.commit()
except Exception as e:
    print(f"⚠️ Warning: Could not pre-populate teams: {e}")
finally:
    db.close()

app = FastAPI(title="CH Project Tracker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://project-tracker-k3h2.onrender.com","http://localhost:5173","http://localhost:5174"],
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