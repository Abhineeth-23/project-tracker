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

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, company: Optional[str] = None, db: Session = Depends(get_db)):
    if company:
        m = models.get_company_models(company)
        db_user = db.query(m["User"]).filter(m["User"].id == user_id).first()
    else:
        db_user = db.query(models.CallHealthUser).filter(models.CallHealthUser.id == user_id).first()
        if not db_user:
            db_user = db.query(models.SucceedUser).filter(models.SucceedUser.id == user_id).first()
            
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user_update: schemas.UserUpdate, company: Optional[str] = None, db: Session = Depends(get_db)):
    # Find user in the right physical table
    comp = company or user_update.company
    db_user = None
    if comp:
        m = models.get_company_models(comp)
        db_user = db.query(m["User"]).filter(m["User"].id == user_id).first()
    
    if not db_user:
        db_user = db.query(models.CallHealthUser).filter(models.CallHealthUser.id == user_id).first()
        if not db_user:
            db_user = db.query(models.SucceedUser).filter(models.SucceedUser.id == user_id).first()
            
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_update.name is not None: db_user.name = user_update.name
    if user_update.rollNumber is not None: db_user.rollNumber = user_update.rollNumber.upper()
    if user_update.team is not None: db_user.team = user_update.team
    if user_update.role is not None: db_user.role = user_update.role

    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, company: Optional[str] = None, db: Session = Depends(get_db)):
    db_user = None
    if company:
        m = models.get_company_models(company)
        db_user = db.query(m["User"]).filter(m["User"].id == user_id).first()
    else:
        db_user = db.query(models.CallHealthUser).filter(models.CallHealthUser.id == user_id).first()
        if not db_user:
            db_user = db.query(models.SucceedUser).filter(models.SucceedUser.id == user_id).first()

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