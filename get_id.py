import asyncio
from aiogram import Bot

TOKEN = "8320654376:AAHaBG0HMCv8TCbX975sTfoTiViBpjcxjIc"
CHANNEL_USERNAME = "@bahromhakimi_ai"

async def get_chat_id():
    bot = Bot(token=TOKEN)
    try:
        chat = await bot.get_chat(CHANNEL_USERNAME)
        print(f"CHANNEL_ID={chat.id}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(get_chat_id())
