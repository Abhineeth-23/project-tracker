from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import logs, users

from .database import engine, Base
from .routers import logs

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CH Project Tracker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(logs.router)
app.include_router(users.router)

@app.get("/")
def health_check():
    return {"status":"API is running securely!"}