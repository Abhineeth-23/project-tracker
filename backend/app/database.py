import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv

#SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")

SQLALCHEMY_DATABASE_URL = "postgresql://neondb_owner:npg_AfGUgNLn36ZV@ep-dry-block-a15f13z3-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

engine = create_engine(SQLALCHEMY_DATABASE_URL, 
    pool_pre_ping=True, 
    pool_recycle=300)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()