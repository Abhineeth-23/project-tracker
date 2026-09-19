from sqlalchemy import Column, Integer, String, BigInteger, JSON
from typing import Optional
from .database import Base

# ==========================================
# 0. ABSTRACT MIXINS
# ==========================================
class UserMixin:
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    rollNumber = Column(String, unique=True, index=True)
    team = Column(String)
    role = Column(String, default="user") 
    createdAt = Column(BigInteger)
    password = Column(String)

class TeamMixin:
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class LogMixin:
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
    suggestionType = Column("suggestiontype", String, nullable=True)
    suggestionDescription = Column("suggestiondescription", String, nullable=True)
    suggestionDeadline = Column("suggestiondeadline", String, nullable=True)
    suggestionStatus = Column("suggestionstatus", String, default="Pending")

class HolidayMixin:
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)
    name = Column(String)

class MoMMixin:
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    agenda = Column(String)
    attendees = Column(String, nullable=True)
    content = Column(String, nullable=True)
    created_by = Column(String)
    file_name = Column(String, nullable=True)
    file_path = Column(String, nullable=True)


# ==========================================
# 1. CALLHEALTH PHYSICAL TABLES
# ==========================================
class CallHealthUser(Base, UserMixin):
    __tablename__ = "callhealth_users"
    company = Column(String, default="CallHealth")

class CallHealthTeam(Base, TeamMixin):
    __tablename__ = "callhealth_teams"
    company = Column(String, default="CallHealth")

class CallHealthLog(Base, LogMixin):
    __tablename__ = "callhealth_logs"
    company = Column(String, default="CallHealth")

class CallHealthHoliday(Base, HolidayMixin):
    __tablename__ = "callhealth_holidays"
    company = Column(String, default="CallHealth")

class CallHealthMoM(Base, MoMMixin):
    __tablename__ = "callhealth_moms"
    company = Column(String, default="CallHealth")


# ==========================================
# 2. SUCCEED INTERNATIONAL PHYSICAL TABLES
# ==========================================
class SucceedUser(Base, UserMixin):
    __tablename__ = "succeed_users"
    company = Column(String, default="Succeed International")

class SucceedTeam(Base, TeamMixin):
    __tablename__ = "succeed_teams"
    company = Column(String, default="Succeed International")

class SucceedLog(Base, LogMixin):
    __tablename__ = "succeed_logs"
    company = Column(String, default="Succeed International")

class SucceedHoliday(Base, HolidayMixin):
    __tablename__ = "succeed_holidays"
    company = Column(String, default="Succeed International")

class SucceedMoM(Base, MoMMixin):
    __tablename__ = "succeed_moms"
    company = Column(String, default="Succeed International")


# ==========================================
# 3. LEGACY TABLES (KEPT FOR BACKUP & INTEGRITY)
# ==========================================
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    rollNumber = Column(String, unique=True, index=True)
    team = Column(String)
    role = Column(String, default="user") 
    company = Column(String, default="CallHealth", index=True)
    createdAt = Column(BigInteger)
    password = Column(String)

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
    company = Column(String, default="CallHealth", index=True)
    suggestionType = Column("suggestiontype", String, nullable=True)
    suggestionDescription = Column("suggestiondescription", String, nullable=True)
    suggestionDeadline = Column("suggestiondeadline", String, nullable=True)
    suggestionStatus = Column("suggestionstatus", String, default="Pending")

class Holiday(Base):
    __tablename__ = "holidays"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)
    name = Column(String)
    company = Column(String, default="CallHealth", index=True)

class MoM(Base):
    __tablename__ = "moms"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    agenda = Column(String)
    attendees = Column(String, nullable=True)
    content = Column(String, nullable=True)
    created_by = Column(String)
    file_name = Column(String, nullable=True)
    file_path = Column(String, nullable=True)
    company = Column(String, default="CallHealth", index=True)

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    company = Column(String, default="CallHealth", index=True)


# ==========================================
# 4. DYNAMIC COMPANY RESOLVER
# ==========================================
def get_company_models(company: Optional[str] = None):
    comp = (company or "CallHealth").strip().lower()
    if "succeed" in comp:
        return {
            "User": SucceedUser,
            "Team": SucceedTeam,
            "Log": SucceedLog,
            "Holiday": SucceedHoliday,
            "MoM": SucceedMoM,
            "company_name": "Succeed International"
        }
    return {
        "User": CallHealthUser,
        "Team": CallHealthTeam,
        "Log": CallHealthLog,
        "Holiday": CallHealthHoliday,
        "MoM": CallHealthMoM,
        "company_name": "CallHealth"
    }