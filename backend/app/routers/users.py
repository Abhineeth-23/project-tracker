import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if the roll number is already in the database
    existing_user = db.query(models.User).filter(models.User.rollNumber == user.rollNumber.upper()).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Roll number already exists")
    
    # Create the new user
    new_user = models.User(
        name=user.name,
        rollNumber=user.rollNumber.upper(), # Always store uppercase
        team=user.team,
        role="user",
        createdAt=int(time.time() * 1000)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=schemas.UserResponse)
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    # Look up the user
    db_user = db.query(models.User).filter(models.User.rollNumber == user.rollNumber.upper()).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

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