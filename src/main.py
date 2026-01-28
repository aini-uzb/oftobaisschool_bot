import asyncio
import logging
import os
import signal
import subprocess
import sys
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# --- FORCE SINGLE INSTANCE ---
def force_single_instance():
    try:
        # Get current PID
        my_pid = os.getpid()
        # List all processes
        result = subprocess.check_output(['ps', '-A', '-o', 'pid,command'], text=True)
        
        for line in result.splitlines():
            if 'src.main' in line and 'python' in line:
                parts = line.strip().split()
                if not parts: continue
                
                try:
                    pid = int(parts[0])
                except ValueError:
                    continue
                    
                if pid != my_pid:
                    print(f"💀 Found stale instance (PID {pid}). Killing it...")
                    try:
                        os.kill(pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    except Exception as e:
                        print(f"Failed to kill {pid}: {e}")
    except Exception as e:
        print(f"Error in single-instance check: {e}")

force_single_instance()
# -----------------------------

from src import config
from src.database.db import init_db
from src.handlers import user_flow, payments, admin, course, homework, survey
from src import scheduler_jobs

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

async def main():
    logging.basicConfig(
        level=logging.DEBUG, 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    print(f"DEBUG: LEADS_GROUP_ID = '{config.LEADS_GROUP_ID}'")
    
    # Initialize Database
    await init_db()
    
    # Initialize Bot and Dispatcher
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())
    
    # Register Routers
    dp.include_router(survey.router)
    dp.include_router(user_flow.router)
    dp.include_router(payments.router)
    dp.include_router(admin.router)
    dp.include_router(course.router)
    dp.include_router(homework.router)
    
    # Scheduler Setup
    # Scheduler Setup
    scheduler = AsyncIOScheduler()
    scheduler_jobs.setup_scheduler(scheduler, bot)
    scheduler.start()
    
    print("🤖 Bot is starting...")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped!")
