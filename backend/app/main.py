from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.db import engine
from app.models.models import Base
from app.api import chat

from app.api import user, meal, water_log, auth
from dotenv import load_dotenv
load_dotenv()
# Load environment variables
    
app = FastAPI(
    title="FitEatBuddy API",
    description="Backend for FitEatBuddy – your AI-powered fitness and nutrition companion",
    version="1.0.0"
)

# Routers
app.include_router(user.router)
app.include_router(meal.router)
app.include_router(water_log.router)
app.include_router(auth.router)
app.include_router(chat.router)

# CORS middleware
origins = ["*"]  # Replace with specific domains in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup DB creation
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created.")

# Root path
@app.get("/")
async def read_root():
    return {"message": "Welcome to FitEatBuddy! Your Buddy is here to help."}