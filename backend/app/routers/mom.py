import os
import time
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from supabase import create_client, Client

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/mom", tags=["Minutes of Meeting"])

# --- SUPABASE INITIALIZATION ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "moms"

UPLOAD_DIR = "uploads/mom"
os.makedirs(UPLOAD_DIR, exist_ok=True)

if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = None
    print("WARNING: Supabase keys not found in environment. Using local storage.")

@router.get("", response_model=List[schemas.MoMResponse], include_in_schema=False)
@router.get("/", response_model=List[schemas.MoMResponse])
def get_moms(company: Optional[str] = None, db: Session = Depends(get_db)):
    """Fetch all MoMs, ordered by newest first"""
    if company:
        m = models.get_company_models(company)
        MoMModel = m["MoM"]
        return db.query(MoMModel).order_by(MoMModel.date.desc(), MoMModel.id.desc()).all()
    else:
        ch = db.query(models.CallHealthMoM).all()
        si = db.query(models.SucceedMoM).all()
        combined = list(ch) + list(si)
        combined.sort(key=lambda x: (x.date or "", x.id or 0), reverse=True)
        return combined

@router.post("/text", response_model=schemas.MoMResponse)
def create_text_mom(mom: schemas.MoMCreateText, db: Session = Depends(get_db)):
    """Create a new MoM using manual text entry"""
    m = models.get_company_models(mom.company)
    MoMModel = m["MoM"]
    company_name = m["company_name"]
    
    new_mom = MoMModel(
        date=mom.date,
        agenda=mom.agenda,
        attendees=mom.attendees,
        content=mom.content,
        created_by=mom.created_by,
        company=company_name
    )
    db.add(new_mom)
    db.commit()
    db.refresh(new_mom)
    return new_mom

@router.post("/upload", response_model=schemas.MoMResponse)
def upload_file_mom(
    date: str = Form(...),
    agenda: str = Form(...),
    attendees: str = Form(""),
    created_by: str = Form(...),
    company: str = Form("CallHealth"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Create a new MoM by uploading a file"""
    if supabase:
        unique_filename = f"{int(time.time())}_{file.filename.replace(' ', '_')}"
        file_bytes = file.file.read()
        res = supabase.storage.from_(BUCKET_NAME).upload(
            path=unique_filename,
            file=file_bytes,
            file_options={"content-type": file.content_type}
        )
        file_path = unique_filename
    else:
        timestamp = int(time.time())
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, safe_filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    m = models.get_company_models(company)
    MoMModel = m["MoM"]
    company_name = m["company_name"]

    new_mom = MoMModel(
        date=date,
        agenda=agenda,
        attendees=attendees,
        file_path=file_path,
        file_name=file.filename,
        created_by=created_by,
        company=company_name
    )
    db.add(new_mom)
    db.commit()
    db.refresh(new_mom)
    return new_mom

@router.get("/download/{mom_id}")
def view_mom_file(mom_id: int, company: Optional[str] = None, db: Session = Depends(get_db)):
    """View or download an uploaded MoM file"""
    mom = None
    if company:
        m = models.get_company_models(company)
        mom = db.query(m["MoM"]).filter(m["MoM"].id == mom_id).first()
        
    if not mom:
        mom = db.query(models.CallHealthMoM).filter(models.CallHealthMoM.id == mom_id).first()
        if not mom:
            mom = db.query(models.SucceedMoM).filter(models.SucceedMoM.id == mom_id).first()
            
    if not mom or not mom.file_path:
        raise HTTPException(status_code=404, detail="File record not found in database")
    
    if supabase:
        public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(mom.file_path)
        return RedirectResponse(url=public_url)
    else:
        if not os.path.exists(mom.file_path):
            raise HTTPException(status_code=404, detail="File not found")
        return FileResponse(
            path=mom.file_path, 
            filename=mom.file_name,
            content_disposition_type="inline" 
        )

@router.delete("/{mom_id}")
def delete_mom(mom_id: int, company: Optional[str] = None, db: Session = Depends(get_db)):
    """Delete an MoM record and its file"""
    mom = None
    if company:
        m = models.get_company_models(company)
        mom = db.query(m["MoM"]).filter(m["MoM"].id == mom_id).first()
        
    if not mom:
        mom = db.query(models.CallHealthMoM).filter(models.CallHealthMoM.id == mom_id).first()
        if not mom:
            mom = db.query(models.SucceedMoM).filter(models.SucceedMoM.id == mom_id).first()

    if not mom:
        raise HTTPException(status_code=404, detail="MoM not found")
    
    if mom.file_path:
        if supabase:
            try:
                supabase.storage.from_(BUCKET_NAME).remove([mom.file_path])
            except Exception as e:
                print(f"Failed to delete file from Supabase: {e}")
        else:
            if os.path.exists(mom.file_path):
                os.remove(mom.file_path)
        
    db.delete(mom)
    db.commit()
    return {"message": "MoM deleted successfully"}
