import time
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas
from ..utils import send_to_google_sheets # Import our new helper!

router = APIRouter(prefix="/api/logs", tags=["Logs"])

@router.get("/", response_model=List[schemas.LogResponse])
def get_logs(db: Session = Depends(get_db)):
    logs = db.query(models.Log).order_by(models.Log.timestamp.desc()).all()
    return logs

@router.post("/", response_model=schemas.LogResponse)
def create_log(log: schemas.LogCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # 1. Save the new log to Postgres
    new_log = models.Log(
        userId=log.userId,
        name=log.name,
        rollNumber=log.rollNumber,
        team=log.team,
        hours=log.hours,
        todayLog=log.todayLog,
        tomorrowGoal=log.tomorrowGoal,
        date=log.date,
        timestamp=int(time.time() * 1000)
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    
    # 2. Prepare the data for Google Sheets
    # Fetch all logs for this specific team on this specific date to keep the sheet accurate
    team_logs = db.query(models.Log).filter(models.Log.team == log.team, models.Log.date == log.date).all()
    
    formatted_logs = []
    for r in team_logs:
        formatted_logs.append({
            "name": r.name,
            "todayLog": r.todayLog,
            "tomorrowGoal": r.tomorrowGoal,
            # Format the JSON array [1,2,3] into a string "1, 2, 3" for the spreadsheet
            "hours": ", ".join(map(str, r.hours)) if r.hours else "" 
        })
        
    payload = {
        "action": "sync_day",
        "team": log.team,
        "date": log.date,
        "logs": formatted_logs
    }
    
    # 3. Fire and Forget! 
    # This tells FastAPI to run this function after returning the response to the user.
    background_tasks.add_task(send_to_google_sheets, payload)
    
    return new_log

@router.put("/{log_id}")
def update_log(log_id: int, log_update: schemas.LogCreate, db: Session = Depends(get_db)):
    """Update an existing log for a previous date"""
    db_log = db.query(models.Log).filter(models.Log.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Log not found")
    
    # Empty array handling
    if not log_update.hours:
        log_update.hours = []

    # Update the fields
    db_log.hours = log_update.hours
    db_log.todayLog = log_update.todayLog
    db_log.tomorrowGoal = log_update.tomorrowGoal
    
    db.commit()
    db.refresh(db_log)
    return db_log