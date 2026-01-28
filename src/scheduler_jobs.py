from aiogram import Bot
from sqlalchemy import select
from datetime import datetime
from src.database.db import async_session
from src.database.models import User
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

async def broadcast_message(bot: Bot, text_uz: str, text_ru: str):
    """Sends a broadcast message to all users."""
    print(f"Starting broadcast: {text_uz[:20]}...")
    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        
        count = 0
        for user in users:
            try:
                msg = text_uz if user.language == "uz" else text_ru
                await bot.send_message(user.user_id, msg)
                count += 1
                await asyncio.sleep(0.05) # Rate limit protection
            except Exception as e:
                # User blocked bot or other error
                pass
        print(f"Broadcast finished. Sent to {count} users.")

def setup_scheduler(scheduler: AsyncIOScheduler, bot: Bot):
    # Feb 1 - 4 days left
    scheduler.add_job(
        broadcast_message, 
        'date', 
        run_date=datetime(2026, 2, 1, 12, 0, 0), 
        args=[bot, "📅 <b>Vebinargacha 4 kun!</b>\n\nRo'yxatdan o'tdingizmi? 👇", "📅 <b>До вебинара 4 дня!</b>\n\nВы зарегистрировались? 👇"]
    )
    
    # Feb 3 - 2 days left
    scheduler.add_job(
        broadcast_message, 
        'date', 
        run_date=datetime(2026, 2, 3, 12, 0, 0), 
        args=[bot, "🎧 <b>Vebinargacha 2 kun!</b>\n\nAirPods o'ynaymiz! 🎁", "🎧 <b>До вебинара 2 дня!</b>\n\nРазыгрываем AirPods! 🎁"]
    )
    
    # Feb 4 - Tomorrow
    scheduler.add_job(
        broadcast_message, 
        'date', 
        run_date=datetime(2026, 2, 4, 12, 0, 0), 
        args=[bot, "🔥 <b>ERTAGA! Vebinar 19:00 da.</b>\n\nTayyor bo'ling!", "🔥 <b>ЗАВТРА! Вебинар в 19:00.</b>\n\nБудьте готовы!"]
    )
    
    # Feb 5 - 10:00
    scheduler.add_job(
        broadcast_message, 
        'date', 
        run_date=datetime(2026, 2, 5, 10, 0, 0), 
        args=[bot, "🚀 <b>BUGUN KECHQURUN!</b>\n\nLink 18:30 da yuboriladi.", "🚀 <b>СЕГОДНЯ ВЕЧЕРОМ!</b>\n\nСсылка будет в 18:30."]
    )
    
    # Feb 5 - 18:30
    scheduler.add_job(
        broadcast_message, 
        'date', 
        run_date=datetime(2026, 2, 5, 18, 30, 0), 
        args=[bot, "⏰ <b>30 daqiqadan keyin boshlaymiz!</b>\n\nMana link: ...", "⏰ <b>Начинаем через 30 минут!</b>\n\nВот ссылка: ..."]
    )
