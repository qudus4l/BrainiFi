from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .models import Base

DATABASE_URL = "sqlite:///./brainifi.db"
ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./brainifi.db"

engine = create_engine(DATABASE_URL)
async_engine = create_async_engine(ASYNC_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

# Create tables
Base.metadata.create_all(bind=engine)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
