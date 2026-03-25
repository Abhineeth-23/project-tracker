import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from typing import List

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    clean_roll = user_data.rollNumber.strip().upper() # Forces uppercase instantly
    
    if not clean_roll:
        raise HTTPException(status_code=400, detail="Roll number cannot be empty.")
    
    existing_user = db.query(models.User).filter(models.User.rollNumber == clean_roll).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Roll number already registered")
        
    new_user = models.User(
        name=user_data.name,
        rollNumber=clean_roll,
        team=user_data.team,
        password=user_data.password, # Save the password
        role="student"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=schemas.UserResponse)
def login_user(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    clean_roll = credentials.rollNumber.strip().upper() # Case-insensitive check
    
    user = db.query(models.User).filter(models.User.rollNumber == clean_roll).first()
    
    # Check if user exists AND if the password matches exactly (case-sensitive)
    if not user or user.password != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid roll number or password.")
        
    return user

@router.get("/",response_model=List[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query (models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_update.name: db_user.name = user_update.name
    if user_update.rollNumber: db_user.rollNumber = user_update.rollNumber.upper()
    if user_update.team: db_user.team = user_update.team
    if user_update.role: db_user.role = user_update.role

    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

@router.post("/admin-login")
def admin_login(credentials: schemas.AdminLogin):
    """Secure login for the workspace administrator"""
    if credentials.username == "admin" and credentials.password == "Hitam@2026":
        return {
            "id": 0,
            "name": "Administrator",
            "rollNumber": "ADMIN",
            "team": "Management",
            "role": "admin",
            "createdAt": int(time.time() * 1000)
        }
    
    # If the password is wrong, kick them out
    raise HTTPException(status_code=401, detail="Invalid admin credentials")