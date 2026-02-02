import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.database.models import Base

from src import config

# Default to SQLite if DATABASE_URL is not set in env (use config's logic)
DATABASE_URL = config.DATABASE_URL or "sqlite+aiosqlite:///database.db"

# Reformat Postgres URL for asyncpg if needed (Railway provides postgres:// or postgresql:// but SQLAlchemy needs postgresql+asyncpg://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgresql://") and "+asyncpg" not in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

print(f"✅ Using DATABASE_URL: {DATABASE_URL[:50]}...")

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        
        # Add missing columns if they don't exist (for Railway deployment)
        try:
            from sqlalchemy import text
            # Try to add seminar_access_code column
            await conn.execute(text(
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS seminar_access_code VARCHAR"
            ))
            print("✅ Added seminar_access_code column (if missing)")
        except Exception as e:
            print(f"⚠️  seminar_access_code column: {e}")
        
        try:
            # Try to add seminar_payment_confirmed column
            await conn.execute(text(
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS seminar_payment_confirmed BOOLEAN DEFAULT FALSE"
            ))
            print("✅ Added seminar_payment_confirmed column (if missing)")
        except Exception as e:
            print(f"⚠️  seminar_payment_confirmed column: {e}")

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
