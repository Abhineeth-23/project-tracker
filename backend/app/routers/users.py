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