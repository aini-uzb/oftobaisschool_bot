"""
Migration: Add seminar access code fields

Run this script to add the new seminar_access_code and seminar_payment_confirmed fields to the users table.
"""
from sqlalchemy import text
from src.database.db import get_session
import asyncio

async def migrate():
    async for session in get_session():
        # Add seminar_access_code column
        try:
            await session.execute(text(
                "ALTER TABLE users ADD COLUMN seminar_access_code VARCHAR"
            ))
            print("✅ Added seminar_access_code column")
        except Exception as e:
            print(f"⚠️  seminar_access_code column may already exist: {e}")
        
        # Add seminar_payment_confirmed column
        try:
            await session.execute(text(
                "ALTER TABLE users ADD COLUMN seminar_payment_confirmed BOOLEAN DEFAULT FALSE"
            ))
            print("✅ Added seminar_payment_confirmed column")
        except Exception as e:
            print(f"⚠️  seminar_payment_confirmed column may already exist: {e}")
        
        await session.commit()
        print("\n✅ Migration completed!")

if __name__ == "__main__":
    asyncio.run(migrate())
