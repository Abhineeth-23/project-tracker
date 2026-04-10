import os
import time
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import List
from supabase import create_client, Client

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/mom", tags=["Minutes of Meeting"])

# --- SUPABASE INITIALIZATION ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "moms"

# Local upload directory as fallback
UPLOAD_DIR = "uploads/mom"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Only initialize if keys are present (prevents crashes during local testing if env vars are missing)
if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = None
    print("WARNING: Supabase keys not found in environment. Using local storage.")

@router.get("/", response_model=List[schemas.MoMResponse])
def get_moms(db: Session = Depends(get_db)):
    """Fetch all MoMs, ordered by newest first"""
    return db.query(models.MoM).order_by(models.MoM.date.desc(), models.MoM.id.desc()).all()

@router.post("/text", response_model=schemas.MoMResponse)
def create_text_mom(mom: schemas.MoMCreateText, db: Session = Depends(get_db)):
    """Create a new MoM using manual text entry"""
    new_mom = models.MoM(
        date=mom.date,
        agenda=mom.agenda,
        attendees=mom.attendees,
        content=mom.content,
        created_by=mom.created_by
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
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Create a new MoM by uploading a file"""
    if supabase:
        # Use Supabase
        unique_filename = f"{int(time.time())}_{file.filename.replace(' ', '_')}"
        file_bytes = file.file.read()
        res = supabase.storage.from_(BUCKET_NAME).upload(
            path=unique_filename,
            file=file_bytes,
            file_options={"content-type": file.content_type}
        )
        file_path = unique_filename
    else:
        # Fallback to local storage
        timestamp = int(time.time())
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, safe_filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    new_mom = models.MoM(
        date=date,
        agenda=agenda,
        attendees=attendees,
        file_path=file_path,
        file_name=file.filename,
        created_by=created_by
    )
    db.add(new_mom)
    db.commit()
    db.refresh(new_mom)
    return new_mom

@router.get("/download/{mom_id}")
def view_mom_file(mom_id: int, db: Session = Depends(get_db)):
    """View or download an uploaded MoM file"""
    mom = db.query(models.MoM).filter(models.MoM.id == mom_id).first()
    if not mom or not mom.file_path:
        raise HTTPException(status_code=404, detail="File record not found in database")
    
    if supabase:
        # Redirect to Supabase public URL
        public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(mom.file_path)
        return RedirectResponse(url=public_url)
    else:
        # Serve local file
        if not os.path.exists(mom.file_path):
            raise HTTPException(status_code=404, detail="File not found")
        return FileResponse(
            path=mom.file_path, 
            filename=mom.file_name,
            content_disposition_type="inline" 
        )

@router.delete("/{mom_id}")
def delete_mom(mom_id: int, db: Session = Depends(get_db)):
    """Delete an MoM record and its file"""
    mom = db.query(models.MoM).filter(models.MoM.id == mom_id).first()
    if not mom:
        raise HTTPException(status_code=404, detail="MoM not found")
    
    # Clean up the file
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
