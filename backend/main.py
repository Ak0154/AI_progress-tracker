import os
from dotenv import load_dotenv
load_dotenv() 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .DB.db import init_db
from .routes import auth, progress

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup...")
    await init_db()
    print("Database connection initialized.")
    yield

    print("Application shutdown...")

app = FastAPI(
    title="AI Progress Tracker API",
    description="API for tracking user progress and getting AI summaries.",
    version="0.1.0",
    lifespan=lifespan  
)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:5500",  
    "null", 
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(progress.router, prefix="/progress")

@app.get("/", tags=["Root"])
def read_root():
    return {"status": "AI Progress Tracker: made by KHUSHI"}