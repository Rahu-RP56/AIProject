from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from pydantic import BaseModel
from datetime import datetime, timedelta

from app.db.db import get_db
from app.models.models import Meal, User
from app.core.deps import get_current_user

router = APIRouter(prefix="/meals", tags=["Meals"])


# ----- Pydantic Schemas -----
class MealCreate(BaseModel):
    name: str
    calories: float
    protein: float


class MealOut(BaseModel):
    id: int
    name: str
    calories: float
    protein: float
    meal_time: datetime

    class Config:
        orm_mode = True


# ----- API Routes -----
@router.post("/", response_model=MealOut)
async def create_meal(
    meal: MealCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_meal = Meal(
        **meal.dict(),
        user_id=current_user.id,
        meal_time=datetime.utcnow()
    )
    db.add(new_meal)
    await db.commit()
    await db.refresh(new_meal)
    return new_meal


@router.get("/", response_model=List[MealOut])
async def get_all_meals(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Meal).where(Meal.user_id == current_user.id))
    return result.scalars().all()


@router.get("/weekly", response_model=List[MealOut])
async def get_weekly_meals(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    one_week_ago = datetime.utcnow() - timedelta(days=7)
    result = await db.execute(
        select(Meal).where(Meal.user_id == current_user.id, Meal.meal_time >= one_week_ago)
    )
    return result.scalars().all()