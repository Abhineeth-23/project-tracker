from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import logs, users, holidays, mom, teams
from .database import engine, Base, get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy import text

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

@app.get("/api/migrate-db")
def migrate_db(db: Session = Depends(get_db)):
    results = []
    
    # 1. Try to rename lowercase columns to camelCase (if they were created without quotes)
    rename_queries = [
        'ALTER TABLE logs RENAME COLUMN suggestiontype TO "suggestionType";',
        'ALTER TABLE logs RENAME COLUMN suggestiondescription TO "suggestionDescription";',
        'ALTER TABLE logs RENAME COLUMN suggestiondeadline TO "suggestionDeadline";',
        'ALTER TABLE logs RENAME COLUMN suggestionstatus TO "suggestionStatus";'
    ]
    for q in rename_queries:
        try:
            db.execute(text(q))
            results.append(f"Renamed: {q}")
        except Exception as e:
            db.rollback()
            results.append(f"Rename failed: {q} - Error: {str(e)}")
            
    # 2. Try to add them with quotes (if they were never created)
    add_queries = [
        'ALTER TABLE logs ADD COLUMN "suggestionType" VARCHAR;',
        'ALTER TABLE logs ADD COLUMN "suggestionDescription" VARCHAR;',
        'ALTER TABLE logs ADD COLUMN "suggestionDeadline" VARCHAR;',
        'ALTER TABLE logs ADD COLUMN "suggestionStatus" VARCHAR DEFAULT \'Pending\';'
    ]
    for q in add_queries:
        try:
            db.execute(text(q))
            results.append(f"Added: {q}")
        except Exception as e:
            db.rollback()
            results.append(f"Add failed: {q} - Error: {str(e)}")

    db.commit()
    return {"status": "migration executed", "details": results}