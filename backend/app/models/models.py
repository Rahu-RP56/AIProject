from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.db import Base  # ✅ Only import DB dependencies

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    meals = relationship("Meal", back_populates="user")

from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from datetime import datetime

class WaterLog(Base):
    __tablename__ = "water_logs"

    id = Column(Integer, primary_key=True, index=True)
    volume_ml = Column(Float, nullable=False)
    log_time = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    calories = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    meal_time = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="meals")

    