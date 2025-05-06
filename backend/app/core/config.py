import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "FitEatBuddy"
    api_version: str = "1.0.0"
    database_url: str = "postgresql+asyncpg://user:password@localhost/dbname"
    secret_key: str = os.getenv("SECRET_KEY", "mysecretkey")  # Update for prod use
    access_token_expire_minutes: int = 30  # Token expiry time for security
    openai_api_key: str
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    

settings = Settings()