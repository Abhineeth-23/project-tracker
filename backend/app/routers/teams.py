from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from typing import List, Optional

router = APIRouter(prefix="/api/teams", tags=["Teams"])

@router.get("", response_model=List[schemas.TeamResponse], include_in_schema=False)
@router.get("/", response_model=List[schemas.TeamResponse])
def get_teams(company: Optional[str] = None, db: Session = Depends(get_db)):
    m = models.get_company_models(company)
    TeamModel = m["Team"]
    return db.query(TeamModel).order_by(TeamModel.name.asc()).all()

@router.post("", response_model=schemas.TeamResponse, include_in_schema=False)
@router.post("/", response_model=schemas.TeamResponse)
def create_team(team_data: schemas.TeamCreate, db: Session = Depends(get_db)):
    cleaned_name = team_data.name.strip()
    if not cleaned_name:
        raise HTTPException(status_code=400, detail="Team name cannot be empty")
        
    m = models.get_company_models(team_data.company)
    TeamModel = m["Team"]
    company_name = m["company_name"]
    
    existing = db.query(TeamModel).filter(TeamModel.name == cleaned_name).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Team '{cleaned_name}' already exists in {company_name}")
    
    new_team = TeamModel(name=cleaned_name, company=company_name)
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team

@router.delete("/{team_id}")
def delete_team(team_id: int, company: Optional[str] = None, db: Session = Depends(get_db)):
    if company:
        m = models.get_company_models(company)
        TeamModel = m["Team"]
        UserModel = m["User"]
        db_team = db.query(TeamModel).filter(TeamModel.id == team_id).first()
    else:
        m = models.get_company_models("CallHealth")
        TeamModel = m["Team"]
        UserModel = m["User"]
        db_team = db.query(TeamModel).filter(TeamModel.id == team_id).first()
        if not db_team:
            m = models.get_company_models("Succeed International")
            TeamModel = m["Team"]
            UserModel = m["User"]
            db_team = db.query(TeamModel).filter(TeamModel.id == team_id).first()
            
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
        
    db.query(UserModel).filter(UserModel.team == db_team.name).update({UserModel.team: ""})
    db.delete(db_team)
    db.commit()
    return {"message": "Team deleted successfully"}
