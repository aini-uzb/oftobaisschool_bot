from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from src.database.db import get_session
from src.database.models import User, UserProgress, Payment
from src import texts, keyboards, config
from src.data import lessons
import json

router = Router()

async def get_user_language(user_id: int, session):
    result = await session.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()
    return user.language if user else "uz"

async def get_or_create_progress(user_id: int, session):
    result = await session.execute(select(UserProgress).where(UserProgress.user_id == user_id))
    progress = result.scalar_one_or_none()
    if not progress:
        progress = UserProgress(user_id=user_id, current_lesson="0.1", completed_lessons="[]")
        session.add(progress)
        await session.commit()
    return progress

@router.message(F.text.in_([texts.Texts.TEXTS["uz"]["menu_course"], texts.Texts.TEXTS["ru"]["menu_course"]]))
async def open_course_menu(message: Message, state: FSMContext):
    async for session in get_session():
        lang = await get_user_language(message.from_user.id, session)
        
        # Check payment
        user_res = await session.execute(select(User).where(User.user_id == message.from_user.id))
        user = user_res.scalar_one_or_none()
        
        if not user or user.payment_status == "none":
            await message.answer(texts.Texts.get("not_subscribed", lang), reply_markup=keyboards.get_tariffs_keyboard(lang))
            return

        text = "📚 <b>Kurs Modullari</b>\n\nDarslarni ko'rish uchun modulni tanlang:" if lang == "uz" else "📚 <b>Модули курса</b>\n\nВыберите модуль для просмотра уроков:"
        await message.answer(text, reply_markup=keyboards.get_course_modules_keyboard(lang))

@router.callback_query(F.data == "open_course")
async def open_course_callback(callback: CallbackQuery, state: FSMContext):
    async for session in get_session():
        lang = await get_user_language(callback.from_user.id, session)
        text = "📚 <b>Kurs Modullari</b>\n\nDarslarni ko'rish uchun modulni tanlang:" if lang == "uz" else "📚 <b>Модули курса</b>\n\nВыберите модуль для просмотра уроков:"
        await callback.message.edit_text(text, reply_markup=keyboards.get_course_modules_keyboard(lang))

@router.callback_query(F.data.startswith("open_module_"))
async def open_module_callback(callback: CallbackQuery, state: FSMContext):
    mod_id = int(callback.data.split("_")[2])
    async for session in get_session():
        lang = await get_user_language(callback.from_user.id, session)
        
        from src.data.lessons import MODULE_NAMES
        mod_name = MODULE_NAMES.get(mod_id, f"Modul {mod_id}")
        
        text = f"📂 <b>Modul {mod_id}: {mod_name}</b>\n\nDarsni tanlang:" if lang == "uz" else f"📂 <b>Модуль {mod_id}: {mod_name}</b>\n\nВыберите урок:"
        await callback.message.edit_text(text, reply_markup=keyboards.get_module_lessons_keyboard(mod_id, lang))

async def show_lesson(bot: Bot, user_id: int, lesson_id: str, session):
    lang = await get_user_language(user_id, session)
    progress = await get_or_create_progress(user_id, session)
    user = await session.get(User, user_id)
    
    lesson_data = lessons.LESSONS.get(lesson_id)
    if not lesson_data:
        # Handle end/error
        return

    # CHECK 1: Partial payment lock
    if not lesson_data["available_partial"] and user.payment_status == "partial":
        text = texts.Texts.get("lesson_locked", lang).format(amount=f"{config.PRICES['PRO']['half']:,}".replace(",", " ")) 
        await bot.send_message(user_id, text, reply_markup=keyboards.get_lesson_locked_keyboard(lang))
        return
        
    # Update current lesson
    progress.current_lesson = lesson_id
    await session.commit()
    
    # Send Materials
    module_name = lessons.MODULE_NAMES.get(lesson_data["module"], f"Modul {lesson_data['module']}")
    
    caption = (
        f"📚 <b>{module_name} | Dars {lesson_id}</b>\n\n"
        f"<b>{lesson_data['title']}</b>\n\n"
        f"⏱ Davomiylik: {lesson_data['duration']}\n\n"
        f"👇 Video dars:"
    )
    
    await bot.send_message(user_id, caption)
    
    try:
        await bot.copy_message(
            chat_id=user_id,
            from_chat_id=lessons.LESSONS_CHANNEL_ID,
            message_id=lesson_data["message_id"],
            protect_content=True
        )
    except Exception as e:
        await bot.send_message(user_id, f"⚠️ Video yuklanmadi (ID: {lesson_data['message_id']}). Admin bilan bog'laning.")
        print(f"Video error: {e}")

    markup = keyboards.get_lesson_keyboard(lesson_id, lesson_data["has_homework"], lang)
    
    if lesson_data["has_homework"]:
        hw_text = texts.Texts.get("homework_prompt", lang).format(text=lesson_data["homework_text"])
        await bot.send_message(user_id, hw_text, reply_markup=markup)
    else:
         await bot.send_message(user_id, "Darsni ko'rib bo'lgach davom eting 👇", reply_markup=markup)

@router.callback_query(F.data.startswith("lesson_"))
async def open_lesson(callback: CallbackQuery, state: FSMContext, bot: Bot):
    lesson_id = callback.data.split("_")[1]
    await callback.message.delete()
    async for session in get_session():
        await show_lesson(bot, callback.from_user.id, lesson_id, session)

@router.callback_query(F.data.startswith("next_lesson_"))
async def next_lesson(callback: CallbackQuery, state: FSMContext, bot: Bot):
    current_id = callback.data.split("_")[2]
    lesson_data = lessons.LESSONS.get(current_id)
    
    async for session in get_session():
        lang = await get_user_language(callback.from_user.id, session)
        
        # Mark completed
        progress = await get_or_create_progress(callback.from_user.id, session)
        completed = json.loads(progress.completed_lessons)
        if current_id not in completed:
            completed.append(current_id)
            progress.completed_lessons = json.dumps(completed)
            await session.commit()
            
        if not lesson_data or not lesson_data["next_lesson"]:
            await callback.message.answer(texts.Texts.get("course_finished", lang))
            return

        next_id = lesson_data["next_lesson"]
        await callback.message.delete()
        await show_lesson(bot, callback.from_user.id, next_id, session)

