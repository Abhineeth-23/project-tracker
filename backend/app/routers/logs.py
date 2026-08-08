import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/logs", tags=["Logs"])

@router.get("", response_model=List[schemas.LogResponse])
def get_logs(db: Session = Depends(get_db)):
    logs = db.query(models.Log).order_by(models.Log.timestamp.desc()).all()
    return logs

@router.post("", response_model=schemas.LogResponse)
def create_log(log: schemas.LogCreate, db: Session = Depends(get_db)):
    # 1. Save the new log to Postgres/SQLite
    new_log = models.Log(
        userId=log.userId,
        name=log.name,
        rollNumber=log.rollNumber,
        team=log.team,
        hours=log.hours,
        todayLog=log.todayLog,
        tomorrowGoal=log.tomorrowGoal,
        date=log.date,
        timestamp=int(time.time() * 1000),
        suggestionType=log.suggestionType,
        suggestionDescription=log.suggestionDescription,
        suggestionDeadline=log.suggestionDeadline,
        suggestionStatus=log.suggestionStatus or "Pending"
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    
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

@router.patch("/{log_id}/suggestion-status")
def update_suggestion_status(log_id: int, status_update: schemas.SuggestionStatusUpdate, db: Session = Depends(get_db)):
    """Update the status of a suggestion/feature request"""
    db_log = db.query(models.Log).filter(models.Log.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Log not found")
    
    db_log.suggestionStatus = status_update.status
    db.commit()
    db.refresh(db_log)
    return db_log