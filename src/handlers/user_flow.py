from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from sqlalchemy import select, update, func
from src import config, texts, keyboards
from src.database.db import get_session
from src.database.models import User
import asyncio

router = Router()

async def get_or_create_user(user_id: int, username: str, first_name: str, session):
    result = await session.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        user = User(user_id=user_id, username=username, first_name=first_name, language="uz") # Default, but will ask
        session.add(user)
        await session.commit()
    return user

async def get_user_language(user_id: int, session) -> str:
    result = await session.execute(select(User.language).where(User.user_id == user_id))
    lang = result.scalar_one_or_none()
    return lang or "uz"

@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot):
    async for session in get_session():
        user = await get_or_create_user(message.from_user.id, message.from_user.username, message.from_user.first_name, session)
        
        # Always ask for language on /start or if not set? 
        # Let's ask for language if it's the very first interaction or just always for flexibility as requested "at start"
        await message.answer(
            texts.Texts.get("language_select", "uz"), # Default text
            reply_markup=keyboards.get_language_keyboard()
        )

@router.callback_query(F.data.startswith("lang_"))
async def process_language_selection(callback: CallbackQuery):
    lang_code = callback.data.split("_")[1]
    
    async for session in get_session():
        await session.execute(
            update(User).where(User.user_id == callback.from_user.id).values(language=lang_code)
        )
        await session.commit()
    
    # Show Welcome Message
    # Also show Main Menu (Persistent)
    await callback.message.delete()
    
    welcome_text = texts.Texts.get("welcome", lang_code).format(name="Bahrom Hakimi")
    await callback.message.answer(
        welcome_text,
        reply_markup=keyboards.get_subscription_keyboard(lang_code)
    )
    # Send persistent menu
    await callback.message.answer(texts.Texts.get("main_menu_text", lang_code), reply_markup=keyboards.get_main_menu_keyboard(lang_code))


async def check_subscription(bot: Bot, user_id: int, channel_id: str) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        print(f"DEBUG: User {user_id} in {channel_id} status: {member.status}")
        return member.status in ["member", "administrator", "creator"]
    except TelegramBadRequest as e:
        print(f"ERROR: TelegramBadRequest for {user_id} in {channel_id}: {e}")
        # If the bot is not admin, it can't check members in some cases, or if channel is private.
        # Check if the error is "Chat not found" or "Bot is not a member of the channel"
        return False
    except Exception as e:
        print(f"ERROR: Unexpected for {user_id} in {channel_id}: {e}")
        return False

@router.callback_query(F.data == "check_subscription")
async def process_check_subscription(callback: CallbackQuery, bot: Bot):
    async for session in get_session():
        lang = await get_user_language(callback.from_user.id, session)
        
        is_subscribed = await check_subscription(bot, callback.from_user.id, config.CHANNEL_ID)
        
        if is_subscribed:
            await session.execute(
                update(User).where(User.user_id == callback.from_user.id).values(subscribed_channel=True)
            )
            await session.commit()

            await callback.message.delete()
            await callback.message.answer(texts.Texts.get("lesson_intro", lang))
            
            # Lesson 1 (Video) - Msg ID 3
            FREE_CH_ID = -1003444130461 
            try:
                await bot.copy_message(chat_id=callback.from_user.id, from_chat_id=FREE_CH_ID, message_id=3)
            except Exception as e:
                print(f"Error copying Lesson 1: {e}")
                await callback.message.answer("📹 [VIDEO 1 LOADING ERROR]")

            # Materials IMMEDIATELY after Lesson 1
            await callback.message.answer(texts.Texts.get("lesson_materials", lang))
            try:
                # Presentation (Msg 5)
                await bot.copy_message(chat_id=callback.from_user.id, from_chat_id=FREE_CH_ID, message_id=5)
                # Prompts (Msg 8)
                await bot.copy_message(chat_id=callback.from_user.id, from_chat_id=FREE_CH_ID, message_id=8)
            except Exception as e:
                print(f"Error copying materials: {e}")

            await asyncio.sleep(4) 
            await callback.message.answer(texts.Texts.get("lesson_1_ask", lang), reply_markup=keyboards.get_lesson_1_watched_keyboard(lang))
        else:
            await callback.answer(texts.Texts.get("not_subscribed", lang), show_alert=True)
            await callback.message.answer(texts.Texts.get("not_subscribed", lang), reply_markup=keyboards.get_retry_subscription_keyboard(lang))

@router.callback_query(F.data == "get_lesson_2")
async def process_get_lesson_2(callback: CallbackQuery, bot: Bot):
    async for session in get_session():
        lang = await get_user_language(callback.from_user.id, session)
        
        await callback.message.edit_reply_markup(reply_markup=None) 
        await callback.message.answer(texts.Texts.get("lesson_2_intro", lang))
        
        FREE_CH_ID = -1003444130461
        # Lesson 2 (Video) - Msg ID 4
        try:
            await bot.copy_message(chat_id=callback.from_user.id, from_chat_id=FREE_CH_ID, message_id=4)
        except Exception as e:
            print(f"Error copying Lesson 2: {e}")
            await callback.message.answer("📹 [VIDEO 2 LOADING ERROR]")
            
        await asyncio.sleep(2)
        
        
        # Send Outro with "Watched" button to trigger Survey
        await callback.message.answer(texts.Texts.get("lesson_outro", lang), reply_markup=keyboards.get_lesson_2_watched_keyboard(lang))

@router.callback_query(F.data == "offer_mini")
async def process_offer_mini(callback: CallbackQuery):
    await callback.answer("Tez kunda...", show_alert=True) # Placeholder as requested


@router.callback_query(F.data == "watched_lesson")
async def process_watched_lesson(callback: CallbackQuery):
    async for session in get_session():
        lang = await get_user_language(callback.from_user.id, session)
        await session.execute(
            update(User).where(User.user_id == callback.from_user.id).values(watched_free_lesson=True)
        )
        await session.commit()

        await callback.message.edit_text(texts.Texts.get("survey_intro_1", lang), reply_markup=keyboards.get_lesson_watched_keyboard(lang))

@router.callback_query(F.data == "register_webinar")
async def process_register_webinar(callback: CallbackQuery):
    async for session in get_session():
        lang = await get_user_language(callback.from_user.id, session)
        await callback.message.edit_text(texts.Texts.get("webinar_info", lang), reply_markup=keyboards.get_webinar_keyboard(lang))

@router.callback_query(F.data == "confirmed_webinar")
async def process_confirm_webinar(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear() 
        print(f"DEBUG: Processing confirm_webinar for {callback.from_user.id}")
        async for session in get_session():
            lang = await get_user_language(callback.from_user.id, session)
            await session.execute(
                update(User).where(User.user_id == callback.from_user.id).values(registered_webinar=True)
            )
            await session.commit()
            
            # Count participants
            result = await session.execute(select(func.count(User.user_id)).where(User.registered_webinar == True))
            count = result.scalar()
            participant_num = 200 + count
            
            msg_text = texts.Texts.get("webinar_confirmed", lang).format(num=participant_num)
            print(f"DEBUG: Sending confirmed msg: {msg_text[:20]}...")
            await callback.message.edit_text(msg_text, reply_markup=keyboards.get_mini_course_keyboard(lang))
    except Exception as e:
        import traceback
        err = traceback.format_exc()
        print(f"CRITICAL ERROR in confirmed_webinar: {err}")
        await callback.answer(f"❌ ERROR: {str(e)[:180]}", show_alert=True)

@router.callback_query(F.data == "list_mini_courses")
async def list_mini_courses(callback: CallbackQuery):
    async for session in get_session():
         lang = await get_user_language(callback.from_user.id, session)
         text = "🚀 <b>Mini Kurslar (Tez kunda...)</b>\n\n" + ("Tanlang:" if lang == "uz" else "Выберите:")
         await callback.message.edit_text(text, reply_markup=keyboards.get_mini_courses_list_keyboard(lang))
        
@router.callback_query(F.data == "mini_course_1")
async def show_mini_course_1(callback: CallbackQuery):
    async for session in get_session():
         lang = await get_user_language(callback.from_user.id, session)
         
    # Syllabus text
    syllabus = (
        "🎥 <b>Mini Kurs: Birinchi million prosmotr olgan AI videoyingiz</b>\n\n"
        "📜 <b>Mundarija:</b>\n\n"
        "1️⃣ <b>Dars 1:</b> ChatGPT Sirlari\n"
        "2️⃣ <b>Dars 2:</b> Eng kuchli video generator - Kling AI\n"
        "3️⃣ <b>Dars 3:</b> Motion Control - Kamera Harakatlari\n"
        "4️⃣ <b>Dars 4:</b> Image-to-Video (Frame to Frame) texnikalari\n"
        "5️⃣ <b>Dars 5:</b> Text-to-Video Texnikalar\n\n"
        "<i>(Darslar tez orada yuklanadi...)</i>"
    )
    
    # Back button to list
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="list_mini_courses"))
    
    await callback.message.edit_text(syllabus, reply_markup=builder.as_markup())

@router.callback_query(F.data == "delete_msg")
async def delete_msg_handler(callback: CallbackQuery):
    await callback.message.delete()

from aiogram.fsm.context import FSMContext

# ... imports ...

async def cleanup_user_request(message: Message, state: FSMContext, bot: Bot):
    """Deletes the user's message and the previous bot reply if stored."""
    # Delete User's message
    try:
        await message.delete()
    except:
        pass
    
    # Delete previous bot message
    data = await state.get_data()
    last_msg_id = data.get("last_bot_msg_id")
    if last_msg_id:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=last_msg_id)
        except:
            pass

async def send_and_track(message: Message, state: FSMContext, text: str, reply_markup=None):
    """Sends a message and tracks its ID in state."""
    msg = await message.answer(text, reply_markup=reply_markup)
    await state.update_data(last_bot_msg_id=msg.message_id)
    return msg

# --- REPLY KEYBOARD HANDLERS ---
@router.message(F.text.in_({"💰 Тарифлар", "💰 Тарифы", "💰 Tariflar"}))
async def menu_tariffs(message: Message, state: FSMContext, bot: Bot):
    await cleanup_user_request(message, state, bot)
    async for session in get_session():
        lang = await get_user_language(message.from_user.id, session)
        await send_and_track(
            message, state,
            text=texts.Texts.get("tariffs_desc", lang),
            reply_markup=keyboards.get_tariffs_keyboard(lang)
        )

@router.message(F.text.in_({"📅 Вебинар", "📅 Vebinar"}))
async def menu_webinar(message: Message, state: FSMContext, bot: Bot):
     await cleanup_user_request(message, state, bot)
     async for session in get_session():
        lang = await get_user_language(message.from_user.id, session)
        await send_and_track(
            message, state,
            text=texts.Texts.get("webinar_info", lang),
            reply_markup=keyboards.get_webinar_keyboard(lang)
        )

@router.message(F.text.in_({"🎓 Бепул дарс", "🎓 Урок", "🎓 Dars", "🎓 Bepul dars"}))
async def menu_lesson(message: Message, state: FSMContext, bot: Bot):
     await cleanup_user_request(message, state, bot)
     async for session in get_session():
        lang = await get_user_language(message.from_user.id, session)
        # For lesson, we might not want to track the *stream* of messages, 
        # but we can track the first interaction or the last one.
        # Let's just send normally as it is a sequence.
        # But we still delete the USER request.
        await message.answer(
            texts.Texts.get("welcome", lang).format(name="Bahrom Hakimi"),
            reply_markup=keyboards.get_subscription_keyboard(lang)
        )

@router.message(F.text.in_({"❓ Ёрдам", "❓ Помощь", "❓ Yordam"}))
async def menu_support(message: Message, state: FSMContext, bot: Bot):
    await cleanup_user_request(message, state, bot)
    await send_and_track(message, state, "@oftobaischoolsupport")

@router.message(F.text.in_({"🚀 Mini kurslar", "🚀 Мини-курсы"}))
async def menu_mini_courses(message: Message, state: FSMContext, bot: Bot):
    await cleanup_user_request(message, state, bot)
    async for session in get_session():
        lang = await get_user_language(message.from_user.id, session)
        text = "🚀 <b>Mini Kurslar</b>\n\nTanlang:" if lang == "uz" else "🚀 <b>Мини-курсы</b>\n\nВыберите:"
        await send_and_track(
            message, state,
            text=text,
            reply_markup=keyboards.get_mini_courses_list_keyboard(lang)
        )
