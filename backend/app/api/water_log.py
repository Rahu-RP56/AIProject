from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from pydantic import BaseModel
from app.models.models import WaterLog,User
from app.db.db import get_db
from datetime import datetime
from app.core.deps import get_current_user
from datetime import datetime, timedelta

router = APIRouter(prefix="/water-logs", tags=["Water Logs"])

class WaterLogCreate(BaseModel):
    volume_ml: float


class WaterLogOut(BaseModel):
    id: int
    volume_ml: float
    log_time: datetime

    class Config:
        orm_mode = True

@router.post("/", response_model=WaterLogOut)
async def create_water_log(
    log: WaterLogCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_log = WaterLog(
        **log.dict(),
        user_id=current_user.id
    )
    db.add(new_log)
    await db.commit()
    await db.refresh(new_log)
    return new_log

@router.get("/", response_model=List[WaterLogOut])
async def get_water_logs(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(WaterLog).where(WaterLog.user_id == current_user.id))
    return result.scalars().all()

@router.get("/weekly", response_model=List[WaterLogOut])
async def get_weekly_logs(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    one_week_ago = datetime.utcnow() - timedelta(days=7)
    result = await db.execute(
        select(WaterLog).where(WaterLog.user_id == current_user.id, WaterLog.log_time >= one_week_ago)
    )
    return result.scalars().all()