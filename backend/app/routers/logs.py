import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/logs", tags=["Logs"])

@router.get("", response_model=List[schemas.LogResponse], include_in_schema=False)
@router.get("/", response_model=List[schemas.LogResponse])
def get_logs(company: Optional[str] = None, db: Session = Depends(get_db)):
    if company:
        m = models.get_company_models(company)
        LogModel = m["Log"]
        return db.query(LogModel).order_by(LogModel.timestamp.desc()).all()
    else:
        ch = db.query(models.CallHealthLog).all()
        si = db.query(models.SucceedLog).all()
        combined = list(ch) + list(si)
        combined.sort(key=lambda x: x.timestamp or 0, reverse=True)
        return combined

@router.post("", response_model=schemas.LogResponse, include_in_schema=False)
@router.post("/", response_model=schemas.LogResponse)
def create_log(log: schemas.LogCreate, db: Session = Depends(get_db)):
    m = models.get_company_models(log.company)
    LogModel = m["Log"]
    company_name = m["company_name"]
    
    new_log = LogModel(
        userId=log.userId,
        name=log.name,
        rollNumber=log.rollNumber,
        team=log.team,
        company=company_name,
        hours=log.hours or [],
        todayLog=log.todayLog or "",
        tomorrowGoal=log.tomorrowGoal or "",
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
def update_log(log_id: int, log_update: schemas.LogCreate, company: Optional[str] = None, db: Session = Depends(get_db)):
    """Update an existing log for a previous date"""
    db_log = None
    comp = company or log_update.company
    if comp:
        m = models.get_company_models(comp)
        db_log = db.query(m["Log"]).filter(m["Log"].id == log_id).first()
        
    if not db_log:
        db_log = db.query(models.CallHealthLog).filter(models.CallHealthLog.id == log_id).first()
        if not db_log:
            db_log = db.query(models.SucceedLog).filter(models.SucceedLog.id == log_id).first()
            
    if not db_log:
        raise HTTPException(status_code=404, detail="Log not found")
    
    if not log_update.hours:
        log_update.hours = []

    db_log.hours = log_update.hours
    db_log.todayLog = log_update.todayLog
    db_log.tomorrowGoal = log_update.tomorrowGoal
    
    db.commit()
    db.refresh(db_log)
    return db_log

@router.patch("/{log_id}/suggestion-status")
def update_suggestion_status(log_id: int, status_update: schemas.SuggestionStatusUpdate, company: Optional[str] = None, db: Session = Depends(get_db)):
    """Update the status of a suggestion/feature request"""
    db_log = None
    if company:
        m = models.get_company_models(company)
        db_log = db.query(m["Log"]).filter(m["Log"].id == log_id).first()
        
    if not db_log:
        db_log = db.query(models.CallHealthLog).filter(models.CallHealthLog.id == log_id).first()
        if not db_log:
            db_log = db.query(models.SucceedLog).filter(models.SucceedLog.id == log_id).first()
            
    if not db_log:
        raise HTTPException(status_code=404, detail="Log not found")
    
    db_log.suggestionStatus = status_update.status
    db.commit()
    db.refresh(db_log)
    return db_log