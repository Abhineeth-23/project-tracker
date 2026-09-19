import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from typing import List, Optional

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    clean_roll = user_data.rollNumber.strip().upper()
    if not clean_roll:
        raise HTTPException(status_code=400, detail="Roll number cannot be empty.")
    
    # Check uniqueness across both physical tables
    ch_exists = db.query(models.CallHealthUser).filter(models.CallHealthUser.rollNumber == clean_roll).first()
    si_exists = db.query(models.SucceedUser).filter(models.SucceedUser.rollNumber == clean_roll).first()
    if ch_exists or si_exists:
        raise HTTPException(status_code=400, detail="Roll number already registered")
        
    m = models.get_company_models(user_data.company)
    UserModel = m["User"]
    company_name = m["company_name"]
    
    new_user = UserModel(
        name=user_data.name,
        rollNumber=clean_roll,
        team=user_data.team or "",
        company=company_name,
        password=user_data.password,
        role="student",
        createdAt=int(time.time() * 1000)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/admin-create-student", response_model=schemas.UserResponse)
def admin_create_student(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    clean_roll = user_data.rollNumber.strip().upper()
    if not clean_roll:
        raise HTTPException(status_code=400, detail="Roll number cannot be empty.")
    
    ch_exists = db.query(models.CallHealthUser).filter(models.CallHealthUser.rollNumber == clean_roll).first()
    si_exists = db.query(models.SucceedUser).filter(models.SucceedUser.rollNumber == clean_roll).first()
    if ch_exists or si_exists:
        raise HTTPException(status_code=400, detail="Roll number already registered")
        
    m = models.get_company_models(user_data.company)
    UserModel = m["User"]
    company_name = m["company_name"]
    
    new_user = UserModel(
        name=user_data.name,
        rollNumber=clean_roll,
        team=user_data.team or "",
        company=company_name,
        password=user_data.password,
        role="student",
        createdAt=int(time.time() * 1000)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=schemas.UserResponse)
def login_user(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    clean_roll = credentials.rollNumber.strip().upper()
    
    # 1. Check CallHealth physical table
    user_ch = db.query(models.CallHealthUser).filter(models.CallHealthUser.rollNumber == clean_roll).first()
    if user_ch:
        if user_ch.password != credentials.password:
            raise HTTPException(status_code=401, detail="Invalid roll number or password.")
        return user_ch
        
    # 2. Check Succeed International physical table
    user_si = db.query(models.SucceedUser).filter(models.SucceedUser.rollNumber == clean_roll).first()
    if user_si:
        if user_si.password != credentials.password:
            raise HTTPException(status_code=401, detail="Invalid roll number or password.")
        return user_si
        
    raise HTTPException(status_code=401, detail="Invalid roll number or password.")

@router.get("", response_model=List[schemas.UserResponse], include_in_schema=False)
@router.get("/", response_model=List[schemas.UserResponse])
def get_all_users(company: Optional[str] = None, db: Session = Depends(get_db)):
    if company:
        m = models.get_company_models(company)
        UserModel = m["User"]
        return db.query(UserModel).all()
    else:
        # Concatenate users from both physical tables
        ch_users = db.query(models.CallHealthUser).all()
        si_users = db.query(models.SucceedUser).all()
        return list(ch_users) + list(si_users)

def _find_user(identifier: str, company: Optional[str], db: Session):
    clean_id = identifier.strip()
    is_numeric = clean_id.isdigit()
    
    if company:
        m = models.get_company_models(company)
        UserModel = m["User"]
        if is_numeric:
            u = db.query(UserModel).filter(UserModel.id == int(clean_id)).first()
            if u: return u
        return db.query(UserModel).filter(UserModel.rollNumber == clean_id.upper()).first()
    else:
        # Check CallHealth first
        if is_numeric:
            u = db.query(models.CallHealthUser).filter(models.CallHealthUser.id == int(clean_id)).first()
            if u: return u
        u = db.query(models.CallHealthUser).filter(models.CallHealthUser.rollNumber == clean_id.upper()).first()
        if u: return u
        
        # Check Succeed
        if is_numeric:
            u = db.query(models.SucceedUser).filter(models.SucceedUser.id == int(clean_id)).first()
            if u: return u
        return db.query(models.SucceedUser).filter(models.SucceedUser.rollNumber == clean_id.upper()).first()

@router.get("/{identifier}", response_model=schemas.UserResponse)
def get_user(identifier: str, company: Optional[str] = None, db: Session = Depends(get_db)):
    db_user = _find_user(identifier, company, db)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{identifier}", response_model=schemas.UserResponse)
def update_user(identifier: str, user_update: schemas.UserUpdate, company: Optional[str] = None, db: Session = Depends(get_db)):
    comp = company or user_update.company
    db_user = _find_user(identifier, comp, db)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_update.name is not None: db_user.name = user_update.name
    if user_update.rollNumber is not None: db_user.rollNumber = user_update.rollNumber.upper()
    if user_update.team is not None: db_user.team = user_update.team
    if user_update.role is not None: db_user.role = user_update.role

    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{identifier}")
def delete_user(identifier: str, company: Optional[str] = None, db: Session = Depends(get_db)):
    db_user = _find_user(identifier, company, db)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

@router.post("/admin-login")
def admin_login(credentials: schemas.AdminLogin):
    """Secure login for the workspace administrator and viewers"""
    if credentials.username == "admin" and credentials.password == "Hitam@2026":
        return {
            "id": 0,
            "name": "Administrator",
            "rollNumber": "ADMIN",
            "team": "Management",
            "role": "admin",
            "createdAt": int(time.time() * 1000)
        }
    elif credentials.username == "viewer" and credentials.password == "View@2026":
        return {
            "id": -1,
            "name": "Executive",
            "rollNumber": "VIEWER",
            "team": "Management",
            "role": "viewer",
            "createdAt": int(time.time() * 1000)
        }
    
    raise HTTPException(status_code=401, detail="Invalid admin or viewer credentials")