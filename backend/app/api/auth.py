from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordRequestForm
from app.models.models import User
from app.db.db import get_db
from app.core.auth import hash_password, verify_password, create_access_token
from pydantic import BaseModel
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password)
    )
    db.add(new_user)
    await db.commit()
    return {"msg": "User created successfully"}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=30)
        
    )
    return {"access_token": token, "token_type": "bearer"}