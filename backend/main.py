import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# ✅ Load environment variables
load_dotenv()

# ✅ Use absolute imports (important for Render)
from backend.DB.db import init_db
from backend.routes import auth, progress

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Application startup...")
    await init_db()
    print("✅ Database connection initialized.")
    yield
    print("🛑 Application shutdown...")

# ✅ Initialize FastAPI app
app = FastAPI(
    title="AI Progress Tracker API",
    description="API for tracking user progress and getting AI summaries.",
    version="0.1.0",
    lifespan=lifespan
)

# ✅ Allow CORS from anywhere (good for testing & public frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],           # Allow all HTTP methods
    allow_headers=["*"],           # Allow all headers
)

# ✅ Include routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(progress.router, prefix="/progress")

@app.get("/", tags=["Root"])
def read_root():
    return {"status": "AI Progress Tracker: made by KHUSHI"}
