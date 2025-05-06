from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.db import get_db
from app.models.models import User
from pydantic import BaseModel, EmailStr
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str  # Should be hashed

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

@router.post("/", response_model=UserOut)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if user already exists
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=user.password  # 🔐 Replace with hash in production
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[UserOut])
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()