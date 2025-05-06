from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Define SQLAlchemy async database URL from your .env file
SQLALCHEMY_DATABASE_URL = settings.database_url

# Create async engine
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

# Async session factory
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()

# Dependency to be used in routes
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session