from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/holidays", tags=["Holidays"])

@router.get("", response_model=List[schemas.HolidayResponse], include_in_schema=False)
@router.get("/", response_model=List[schemas.HolidayResponse])
def get_holidays(company: Optional[str] = None, db: Session = Depends(get_db)):
    """Fetch all declared holidays for the company or all companies"""
    if company:
        m = models.get_company_models(company)
        HolidayModel = m["Holiday"]
        return db.query(HolidayModel).order_by(HolidayModel.date.desc()).all()
    else:
        ch = db.query(models.CallHealthHoliday).all()
        si = db.query(models.SucceedHoliday).all()
        combined = list(ch) + list(si)
        combined.sort(key=lambda x: x.date or "", reverse=True)
        return combined

@router.post("", response_model=schemas.HolidayResponse, include_in_schema=False)
@router.post("/", response_model=schemas.HolidayResponse)
def create_holiday(holiday: schemas.HolidayCreate, db: Session = Depends(get_db)):
    """Declare a new holiday"""
    company_name = (holiday.company or "CallHealth").strip()
    
    if company_name.lower() == "all":
        # Add to both CallHealth and Succeed tables
        for ModelClass, comp in [(models.CallHealthHoliday, "CallHealth"), (models.SucceedHoliday, "Succeed International")]:
            exists = db.query(ModelClass).filter(ModelClass.date == holiday.date).first()
            if not exists:
                db.add(ModelClass(date=holiday.date, name=holiday.name, company=comp))
        db.commit()
        return schemas.HolidayResponse(id=0, date=holiday.date, name=holiday.name, company="All")
    
    m = models.get_company_models(company_name)
    HolidayModel = m["Holiday"]
    resolved_comp = m["company_name"]
    
    existing = db.query(HolidayModel).filter(HolidayModel.date == holiday.date).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"A holiday is already declared on this date for {resolved_comp}.")
    
    new_holiday = HolidayModel(date=holiday.date, name=holiday.name, company=resolved_comp)
    db.add(new_holiday)
    db.commit()
    db.refresh(new_holiday)
    return new_holiday

@router.delete("/{holiday_id}")
def delete_holiday(holiday_id: int, company: Optional[str] = None, db: Session = Depends(get_db)):
    """Delete a holiday"""
    db_holiday = None
    if company:
        m = models.get_company_models(company)
        db_holiday = db.query(m["Holiday"]).filter(m["Holiday"].id == holiday_id).first()
        
    if not db_holiday:
        db_holiday = db.query(models.CallHealthHoliday).filter(models.CallHealthHoliday.id == holiday_id).first()
        if not db_holiday:
            db_holiday = db.query(models.SucceedHoliday).filter(models.SucceedHoliday.id == holiday_id).first()
            
    if not db_holiday:
        raise HTTPException(status_code=404, detail="Holiday not found")
    
    db.delete(db_holiday)
    db.commit()
    return {"message": "Holiday removed successfully"}