from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from ..database import get_db
from .. import models, schemas
import time

router = APIRouter(prefix="/api/mom", tags=["Minutes of Meet"])

UPLOAD_DIR = "uploads/mom"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/", response_model=List[schemas.MoMResponse])
def get_moms(db: Session = Depends(get_db)):
    return db.query(models.MoM).order_by(models.MoM.id.desc()).all()

@router.post("/text", response_model=schemas.MoMResponse)
def create_mom_text(mom: schemas.MoMCreateText, db: Session = Depends(get_db)):
    db_mom = models.MoM(
        date=mom.date,
        agenda=mom.agenda,
        attendees=mom.attendees,
        content=mom.content,
        created_by=mom.created_by
    )
    db.add(db_mom)
    db.commit()
    db.refresh(db_mom)
    return db_mom

@router.post("/upload", response_model=schemas.MoMResponse)
def create_mom_upload(
    date: str = Form(...),
    agenda: str = Form(...),
    created_by: str = Form(...),
    attendees: str = Form(""),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    timestamp = int(time.time())
    safe_filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    db_mom = models.MoM(
        date=date,
        agenda=agenda,
        attendees=attendees,
        created_by=created_by,
        file_name=file.filename,
        file_path=file_path
    )
    db.add(db_mom)
    db.commit()
    db.refresh(db_mom)
    return db_mom

@router.get("/download/{mom_id}")
def download_mom_file(mom_id: int, db: Session = Depends(get_db)):
    """Download or preview an uploaded MoM file"""
    mom = db.query(models.MoM).filter(models.MoM.id == mom_id).first()
    if not mom or not mom.file_path or not os.path.exists(mom.file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # NEW: Added content_disposition_type="inline"
    return FileResponse(
        path=mom.file_path, 
        filename=mom.file_name,
        content_disposition_type="inline" 
    )

@router.delete("/{mom_id}")
def delete_mom(mom_id: int, db: Session = Depends(get_db)):
    mom = db.query(models.MoM).filter(models.MoM.id == mom_id).first()
    if not mom:
        raise HTTPException(status_code=404, detail="MoM not found")
        
    # Delete file if exists
    if mom.file_path and os.path.exists(mom.file_path):
        os.remove(mom.file_path)
        
    db.delete(mom)
    db.commit()
    return {"message": "MoM deleted successfully"}
