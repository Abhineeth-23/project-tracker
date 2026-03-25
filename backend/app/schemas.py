from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    name: str
    rollNumber: str
    team: str

class UserLogin(BaseModel):
    rollNumber: str

class UserResponse(BaseModel):
    id: int
    name: str
    rollNumber: str
    team: str
    role: str
    
    model_config = {"from_attributes": True} 

class LogCreate(BaseModel):
    userId: int
    name: str
    rollNumber: str
    team: str
    hours: List[int] = []
    todayLog: Optional[str] = ""
    tomorrowGoal: Optional[str] = ""
    date: str

class LogResponse(LogCreate):
    id: int
    timestamp: int
    
    model_config = {"from_attributes": True}

class UserUpdate(BaseModel):
    name: Optional[str] = None
    rollNumber: Optional[str] = None
    team: Optional[str] = None
    role: Optional[str] = None

class HolidayCreate(BaseModel):
    date: str
    name: str

class HolidayResponse(BaseModel):
    id: int
    date: str
    name: str

    class Config:
        from_attributes = True

class AdminLogin(BaseModel):
    username: str
    password: str