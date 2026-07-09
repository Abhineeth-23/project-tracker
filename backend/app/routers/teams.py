from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from typing import List

router = APIRouter(prefix="/api/teams", tags=["Teams"])

@router.get("/", response_model=List[schemas.TeamResponse])
def get_teams(db: Session = Depends(get_db)):
    return db.query(models.Team).order_by(models.Team.name.asc()).all()

@router.post("/", response_model=schemas.TeamResponse)
def create_team(team_data: schemas.TeamCreate, db: Session = Depends(get_db)):
    cleaned_name = team_data.name.strip()
    if not cleaned_name:
        raise HTTPException(status_code=400, detail="Team name cannot be empty")
        
    existing = db.query(models.Team).filter(models.Team.name == cleaned_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Team name already exists")
    
    new_team = models.Team(name=cleaned_name)
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    
    return new_team

@router.delete("/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db)):
    db_team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # 1. Update all users assigned to this team to be unassigned ("")
    db.query(models.User).filter(models.User.team == db_team.name).update({models.User.team: ""})
    
    # 2. Update all historical logs with this team to be unassigned ("")
    db.query(models.Log).filter(models.Log.team == db_team.name).update({models.Log.team: ""})
    
    db.delete(db_team)
    db.commit()
    return {"message": "Team deleted successfully"}
