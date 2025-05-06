from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.db.db import get_db
from app.models.models import User, WaterLog, Meal
from app.core.deps import get_current_user
from app.core.config import settings
from openai import OpenAI



router = APIRouter(prefix="/chat", tags=["Buddy AI"])

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

client = OpenAI(api_key=settings.openai_api_key)

@router.post("/", response_model=ChatResponse)
async def chat_with_buddy(
    req: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = datetime.utcnow().date()

    meals = await db.execute(
        Meal.__table__.select().where(Meal.user_id == current_user.id)
    )
    meals = meals.fetchall()

    water_logs = await db.execute(
        WaterLog.__table__.select().where(WaterLog.user_id == current_user.id)
    )
    water_logs = water_logs.fetchall()

    total_water = sum(w.volume_ml for w in water_logs)
    total_calories = sum(m.calories for m in meals)
    total_protein = sum(m.protein for m in meals)

    messages = [
        {
            "role": "system",
            "content": (
                "You are Buddy, a friendly AI fitness coach. Be supportive and smart. "
                "You know user's hydration and meal data."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Today I drank {total_water} ml of water and consumed {total_calories} kcal, "
                f"including {total_protein}g of protein. I want to: {req.message}"
            ),
        },
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.8,
        )
        return {"reply": response.choices[0].message.content.strip()}
    except Exception as e:
        return {"reply": f"Error: {str(e)}"}