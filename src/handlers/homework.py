from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select
from src.database.db import get_session
from src.database.models import User, UserProgress, Payment
from src import texts, keyboards, config
from src.data import lessons
import json

router = Router()

class HomeworkState(StatesGroup):
    waiting_for_homework = State()
    waiting_for_feedback = State()

async def get_user_language(user_id: int, session):
    result = await session.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()
    return user.language if user else "uz"

@router.callback_query(F.data.startswith("submit_hw_"))
async def start_homework_submission(callback: CallbackQuery, state: FSMContext):
    lesson_id = callback.data.split("_")[2]
    await state.update_data(hw_lesson_id=lesson_id)
    await state.set_state(HomeworkState.waiting_for_homework)
    
    lesson = lessons.LESSONS.get(lesson_id)
    module_num = lesson["module"]
    
    async for session in get_session():
        lang = await get_user_language(callback.from_user.id, session)
        text = texts.Texts.get("homework_submit_instruction", lang).format(module=module_num, lesson=lesson_id)
        await callback.message.answer(text)
        await callback.answer()

@router.message(HomeworkState.waiting_for_homework)
async def process_homework_upload(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    lesson_id = data.get("hw_lesson_id")
    lesson = lessons.LESSONS.get(lesson_id)
    module_num = lesson["module"]
    
    # Save to DB (update status)
    async for session in get_session():
        # Get progress
        res = await session.execute(select(UserProgress).where(UserProgress.user_id == message.from_user.id))
        progress = res.scalar_one_or_none()
        if progress:
            progress.homework_status = "submitted"
            progress.homework_lesson = lesson_id
            # progress.homework_file_id = ... (save file ID if needed, simplified for now)
            await session.commit()
        
        lang = await get_user_language(message.from_user.id, session)
        
        # User notify
        await message.answer(texts.Texts.get("homework_received", lang))
        
        # Admin notify
        admin_text = (
            f"📥 <b>YANGI DZ</b>\n\n"
            f"👤 Kim: @{message.from_user.username}\n"
            f"🆔 ID: {message.from_user.id}\n"
            f"📚 Dars: {lesson_id} — {lesson['title']}\n"
        )
        
        try:
             # Notify all admins
            for admin_id in config.ADMIN_IDS:
                try:
                    await bot.send_message(admin_id, admin_text)
                    await message.forward(admin_id)
                    
                    await bot.send_message(
                        admin_id, 
                        "👇 Tasdiqlash yoki rad etish:", 
                        reply_markup=keyboards.get_homework_admin_keyboard(message.from_user.id, lesson_id)
                    )
                except Exception as ex:
                     print(f"Failed to notify admin {admin_id}: {ex}")
        except Exception as e:
            print(f"Failed to send HW to admins: {e}")

    await state.clear()

# --- ADMIN ACTIONS ---

@router.callback_query(F.data.startswith("approve_hw_"))
async def approve_homework(callback: CallbackQuery, bot: Bot):
    # data: approve_hw_USERID_LESSONID
    parts = callback.data.split("_")
    user_id = int(parts[2])
    lesson_id = parts[3]
    
    lesson = lessons.LESSONS.get(lesson_id)
    
    async for session in get_session():
        # Update User Progress
        res = await session.execute(select(UserProgress).where(UserProgress.user_id == user_id))
        progress = res.scalar_one_or_none()
        if progress:
            progress.homework_status = "approved"
            completed = json.loads(progress.completed_lessons)
            if lesson_id not in completed:
                completed.append(lesson_id)
                progress.completed_lessons = json.dumps(completed)
            await session.commit()
            
            # Notify User
            lang = await get_user_language(user_id, session)
            text = texts.Texts.get("homework_approved", lang).format(module=lesson["module"])
            
            # Add "Next Module" button or just link to course
            # Assuming next lesson is start of next module or just next lesson
            if lesson["next_lesson"]:
                next_l = lesson["next_lesson"]
                markup = keyboards.InlineKeyboardBuilder()
                markup.row(keyboards.InlineKeyboardButton(text="▶️ Davom etish / Продолжить", callback_data=f"lesson_{next_l}"))
                await bot.send_message(user_id, text, reply_markup=markup.as_markup())
            else:
                 await bot.send_message(user_id, text)

    await callback.message.edit_text(f"✅ DZ tasdiqlandi\nO'quvchi: {user_id}\nDars: {lesson_id}")

@router.callback_query(F.data.startswith("reject_hw_"))
async def reject_homework_start(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split("_")
    user_id = int(parts[2])
    lesson_id = parts[3]
    
    await state.update_data(reject_user_id=user_id, reject_lesson_id=lesson_id)
    await state.set_state(HomeworkState.waiting_for_feedback)
    
    await callback.message.edit_text(f"💬 Feedback yozing (nega qayta topshirish kerak):\nUser: {user_id}")

@router.message(HomeworkState.waiting_for_feedback)
async def process_feedback(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    user_id = data.get("reject_user_id")
    lesson_id = data.get("reject_lesson_id")
    
    feedback = message.text
    
    async for session in get_session():
        # Update Status
        res = await session.execute(select(UserProgress).where(UserProgress.user_id == user_id))
        progress = res.scalar_one_or_none()
        if progress:
            progress.homework_status = "rejected"
            await session.commit()
            
            # Notify User
            lang = await get_user_language(user_id, session)
            text = texts.Texts.get("homework_rejected", lang).format(feedback=feedback)
            
            markup = keyboards.InlineKeyboardBuilder()
            markup.row(keyboards.InlineKeyboardButton(text="📤 Qayta yuborish", callback_data=f"submit_hw_{lesson_id}")) # Go straight to submit
            
            await bot.send_message(user_id, text, reply_markup=markup.as_markup())
            
    await message.answer("✅ Feedback yuborildi.")
    await state.clear()
