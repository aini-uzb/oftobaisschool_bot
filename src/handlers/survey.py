from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from src import texts, keyboards, config
from src.database.db import get_session
from src.database.models import User
from sqlalchemy import select

router = Router()

class SurveyState(StatesGroup):
    waiting_for_q1 = State() # Name
    waiting_for_q2 = State() # Activity
    waiting_for_q3 = State() # AI Knowledge
    waiting_for_q4 = State() # Goal
    waiting_for_q5 = State() # Point A/B
    waiting_for_q6 = State() # Phone

async def get_user_language(user_id: int, session) -> str:
    result = await session.execute(select(User.language).where(User.user_id == user_id))
    lang = result.scalar_one_or_none()
    return lang or "uz"

# --- ENTRY POINT ---

@router.callback_query(F.data == "start_survey_intro")
async def start_survey_flow(callback: CallbackQuery):
    async for session in get_session():
        lang = await get_user_language(callback.from_user.id, session)
        await callback.message.answer(texts.Texts.get("survey_intro_2", lang), reply_markup=keyboards.get_survey_choice_keyboard(lang))
        await callback.answer()

@router.callback_query(F.data == "survey_later")
async def survey_later(callback: CallbackQuery):
    await callback.answer("OK!", show_alert=False)
    await callback.message.delete()

@router.callback_query(F.data == "survey_start_q1")
async def ask_q1(callback: CallbackQuery, state: FSMContext):
    async for session in get_session():
        lang = await get_user_language(callback.from_user.id, session)
        await state.update_data(lang=lang)
        await callback.message.answer(texts.Texts.get("survey_q1", lang), reply_markup=ReplyKeyboardRemove())
        await state.set_state(SurveyState.waiting_for_q1)
        await callback.answer()

# --- ANSWERS ---

@router.message(SurveyState.waiting_for_q1)
async def process_q1(message: Message, state: FSMContext):
    await state.update_data(answer_q1=message.text)
    
    data = await state.get_data()
    lang = data.get("lang", "uz")
    
    await message.answer(texts.Texts.get("survey_q2", lang), reply_markup=keyboards.get_activity_keyboard(lang))
    await state.set_state(SurveyState.waiting_for_q2)

@router.message(SurveyState.waiting_for_q2)
async def process_q2(message: Message, state: FSMContext):
    await state.update_data(answer_q2=message.text)
    
    data = await state.get_data()
    lang = data.get("lang", "uz")
    
    await message.answer(texts.Texts.get("survey_q3", lang), reply_markup=keyboards.get_knowledge_keyboard(lang))
    await state.set_state(SurveyState.waiting_for_q3)

@router.message(SurveyState.waiting_for_q3)
async def process_q3(message: Message, state: FSMContext):
    await state.update_data(answer_q3=message.text)
    
    data = await state.get_data()
    lang = data.get("lang", "uz")
    
    await message.answer(texts.Texts.get("survey_q4", lang), reply_markup=keyboards.get_goal_keyboard(lang))
    await state.set_state(SurveyState.waiting_for_q4)

@router.message(SurveyState.waiting_for_q4)
async def process_q4(message: Message, state: FSMContext):
    await state.update_data(answer_q4=message.text)
    
    data = await state.get_data()
    lang = data.get("lang", "uz")
    
    await message.answer(texts.Texts.get("survey_q5", lang), reply_markup=ReplyKeyboardRemove())
    await state.set_state(SurveyState.waiting_for_q5)

@router.message(SurveyState.waiting_for_q5)
async def process_q5(message: Message, state: FSMContext):
    await state.update_data(answer_q5=message.text)
    
    data = await state.get_data()
    lang = data.get("lang", "uz")
    
    await message.answer(texts.Texts.get("survey_q6", lang), reply_markup=keyboards.get_contact_keyboard(lang))
    await state.set_state(SurveyState.waiting_for_q6)

@router.message(SurveyState.waiting_for_q6)
async def process_q6(message: Message, state: FSMContext, bot: Bot):
    # Handle phone number (text or contact)
    phone = message.text
    if message.contact:
        phone = message.contact.phone_number
    
    await state.update_data(answer_q6=phone)
    
    data = await state.get_data()
    lang = data.get("lang", "uz")
    
    # Save/Send Data
    try:
        if config.LEADS_GROUP_ID:
            print(f"DEBUG: Attempting to send report to {config.LEADS_GROUP_ID}")
            report = (
                f"📝 <b>YANGI LEAD (Webinar)</b>\n\n"
                f"👤 <b>User:</b> {message.from_user.full_name} (@{message.from_user.username})\n"
                f"🆔 <b>ID:</b> {message.from_user.id}\n"
                f"🌐 <b>Lang:</b> {lang}\n\n"
                f"1️⃣ <b>Ism:</b> {data.get('answer_q1')}\n"
                f"2️⃣ <b>Faoliyat:</b> {data.get('answer_q2')}\n"
                f"3️⃣ <b>AI:</b> {data.get('answer_q3')}\n"
                f"4️⃣ <b>Maqsad:</b> {data.get('answer_q4')}\n"
                f"5️⃣ <b>A -> B:</b> {data.get('answer_q5')}\n"
                f"6️⃣ <b>Tel:</b> {phone}"
            )
            await bot.send_message(config.LEADS_GROUP_ID, report)
            print("DEBUG: Report sent successfully.")
        else:
            print("WARNING: LEADS_GROUP_ID is not set in config/env!")
    except Exception as e:
        print(f"Failed to send lead to group: {e}")
        
    print("DEBUG: Sending completion message with Main Menu.")
    # 1. Send "Thank you" with Main Menu (Reply Keyboard)
    await message.answer(texts.Texts.get("survey_completed", lang), reply_markup=keyboards.get_main_menu_keyboard(lang))
    
    # 2. Update logic: Use just "Manager will contact" message.
    # The survey_completed text already includes the "Manager will contact" info or we can create a specific one.
    # The existing "survey_completed" in texts.py (lines 566+) in RU version has webinar details! 
    # But wait, user said "after answering the last question ... soon our manager will contact you."
    # The current text `survey_completed` (RU/UZ) has Webinar Info.
    # I should change `survey_completed` text in `texts.py` to be just "Thank you. Manager will contact."
    # BUT FIRST, let's remove the extra message here.
    
    await state.clear()
