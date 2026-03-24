from sqlalchemy import Column, Integer, String, BigInteger, JSON
from .database import Base

# 1. The Accounts Table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    rollNumber = Column(String, unique=True, index=True)
    team = Column(String)
    role = Column(String, default="user") 
    createdAt = Column(BigInteger)

# 2. The Daily Updates Table
class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer)
    name = Column(String)
    rollNumber = Column(String)
    team = Column(String)
    hours = Column(JSON)
    todayLog = Column(String)
    tomorrowGoal = Column(String)
    date = Column(String)
    timestamp = Column(BigInteger)

# 3. The Holidays Table
class Holiday(Base):
    __tablename__ = "holidays"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, unique=True, index=True)
    name = Column(String)