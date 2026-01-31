from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
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
    
    # Show Welcome Message with Photo
    # Also show Main Menu (Persistent)
    await callback.message.delete()
    
    welcome_text = texts.Texts.get("welcome", lang_code)
    
    # Send photo with welcome text as caption
    import os
    photo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "welcome_photo.jpg")
    
    try:
        photo = FSInputFile(photo_path)
        await callback.message.answer_photo(
            photo=photo,
            caption=welcome_text,
            reply_markup=keyboards.get_subscription_keyboard(lang_code)
        )
    except Exception as e:
        print(f"Error sending welcome photo: {e}")
        # Fallback to text only
        await callback.message.answer(
            welcome_text,
            reply_markup=keyboards.get_subscription_keyboard(lang_code)
        )
    
    # Send persistent menu with 3 buttons
    await callback.message.answer(texts.Texts.get("main_menu_text", lang_code), reply_markup=keyboards.get_welcome_keyboard(lang_code))


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

@router.callback_query(F.data == "check_subscription_lesson")
async def process_check_subscription_lesson(callback: CallbackQuery, bot: Bot):
    # Wrapper for the Lesson check
    await process_check_subscription(callback, bot)

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
    # Upsell to Seminar instead of Mini Course placeholder
    await callback.message.edit_text("🔥 Seminarga marhamat!", reply_markup=keyboards.get_webinar_keyboard("uz"))

@router.callback_query(F.data == "check_subscription_ai")
async def process_check_subscription_ai(callback: CallbackQuery, bot: Bot):
     await menu_ai_services(callback.message, None, bot, from_callback=True, make_new=True)


@router.callback_query(F.data == "watched_lesson")
async def process_watched_lesson(callback: CallbackQuery):
    async for session in get_session():
        lang = await get_user_language(callback.from_user.id, session)
        await session.execute(
            update(User).where(User.user_id == callback.from_user.id).values(watched_free_lesson=True)
        )
        await session.commit()

        # Skip intermediate step (survey_intro_1) as requested and go straight to Survey Intro 2 (Seminar Offer)
        await callback.message.edit_text(texts.Texts.get("survey_intro_2", lang), reply_markup=keyboards.get_survey_choice_keyboard(lang))

@router.callback_query(F.data == "register_webinar")
async def process_register_webinar(callback: CallbackQuery):
    async for session in get_session():
        lang = await get_user_language(callback.from_user.id, session)
        await callback.message.edit_text(texts.Texts.get("webinar_info", lang), reply_markup=keyboards.get_seminar_keyboard(lang))

@router.callback_query(F.data == "confirmed_webinar")
async def process_confirm_webinar(callback: CallbackQuery, state: FSMContext):
    # This might be reachable if we have old buttons or if I decide to keep "Register" 
    # But for now it's effectively dead code or we can redirect to pay. 
    # Let's leave it as is for safety or update it to be clean.
    # The user didn't ask to remove it, but since "Register" button is gone, this is dead code.
    pass

@router.callback_query(F.data == "seminar_pay")
async def process_seminar_pay(callback: CallbackQuery, state: FSMContext):
    try:
        # Import PaymentState here to avoid circular dependency
        from src.handlers.payments import PaymentState
        
        await state.set_state(PaymentState.waiting_for_receipt)
        async for session in get_session():
            lang = await get_user_language(callback.from_user.id, session)
            
            await state.update_data(
                tariff="SEMINAR",
                amount=99000,
                type="ticket",
                lang=lang,
                payment_instruction_msg_id=callback.message.message_id
            )
            
            text = texts.Texts.get("seminar_payment_instructions", lang)
            # Use a simple back button or None
            # keyboards.get_payment_back_keyboard handles generic callbacks, let's use it or make a simple one
            # For now, just None as instructions are inline
            
            builder = keyboards.InlineKeyboardBuilder()
            builder.row(keyboards.InlineKeyboardButton(text="⬅️ " + ("Orqaga" if lang == "uz" else "Назад"), callback_data="register_webinar"))
            
            await callback.message.edit_text(text, reply_markup=builder.as_markup())
            
    except Exception as e:
        import traceback
        err = traceback.format_exc()
        print(f"CRITICAL ERROR in seminar_pay: {err}")
        await callback.answer(f"❌ ERROR: {str(e)[:180]}", show_alert=True)


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

@router.message(F.text.in_({"📅 Вебинар", "📅 Vebinar", "📅 Seminar", "📅 Семинар"}))
async def menu_webinar(message: Message, state: FSMContext, bot: Bot):
     await cleanup_user_request(message, state, bot)
     async for session in get_session():
        lang = await get_user_language(message.from_user.id, session)
        await send_and_track(
            message, state,
            text=texts.Texts.get("webinar_info", lang),
            reply_markup=keyboards.get_seminar_keyboard(lang)
        )

@router.message(F.text.in_({"📅 Seminarga yozilish", "📅 Записаться на семинар"}))
async def menu_seminar_btn(message: Message, state: FSMContext, bot: Bot):
    await menu_webinar(message, state, bot)

@router.message(F.text.in_({"🤖 AI Saytlar (Top 5)", "🤖 AI Сайты (Топ 5)"}))
async def menu_ai_sites_btn(message: Message, state: FSMContext, bot: Bot):
    await menu_ai_services(message, state, bot)

@router.message(F.text.in_({"🎓 Bepul darsni ko'rish", "🎓 Смотреть бесплатный урок"}))
async def menu_free_lesson_btn(message: Message, state: FSMContext, bot: Bot):
    await cleanup_user_request(message, state, bot)
    
    user_id = message.from_user.id
    async for session in get_session():
        lang = await get_user_language(user_id, session)
        
        is_subscribed = await check_subscription(bot, user_id, config.CHANNEL_ID)
        
        if is_subscribed:
            # Manually trigger the "I am subscribed" logic for lesson
           # We can reuse process_check_subscription logic but we need a mock callback or extract logic.
           # Let's extract logic or just create a specific flow here.
           # To save time and keep it clean, let's just copy the success logic from process_check_subscription (lines 107-128)
           # OR better: make a shared function `send_lesson_1(bot, user_id, lang)`
           
           await message.answer(texts.Texts.get("lesson_intro", lang))
           
           FREE_CH_ID = -1003444130461 
           try:
                await bot.copy_message(chat_id=user_id, from_chat_id=FREE_CH_ID, message_id=3)
           except:
                await message.answer("📹 [VIDEO 1 LOADING ERROR]")

           await message.answer(texts.Texts.get("lesson_materials", lang))
           try:
                await bot.copy_message(chat_id=user_id, from_chat_id=FREE_CH_ID, message_id=5)
                await bot.copy_message(chat_id=user_id, from_chat_id=FREE_CH_ID, message_id=8)
           except:
                pass
            
           await asyncio.sleep(4) 
           await message.answer(texts.Texts.get("lesson_1_ask", lang), reply_markup=keyboards.get_lesson_1_watched_keyboard(lang))

        else:
            text = texts.Texts.get("not_subscribed", lang)
            # Use a keyboard that calls "check_subscription_lesson" 
            # We used "check_subscription" for lesson before (line 93).
            # But line 93 logic is exactly what we want.
            
            builder = keyboards.InlineKeyboardBuilder()
            builder.row(keyboards.InlineKeyboardButton(text=("📢 Kanalga o'tish" if lang == "uz" else "📢 Перейти в канал"), url=f"https://t.me/{config.CHANNEL_USERNAME.replace('@', '')}"))
            builder.row(keyboards.InlineKeyboardButton(text=("✅ Obuna bo'ldim" if lang == "uz" else "✅ Я подписался"), callback_data="check_subscription")) # Reusing generic
            
            await message.answer(text, reply_markup=builder.as_markup())
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

@router.message(F.text.in_({"🚀 Mini kurslar", "🚀 Мини-курсы", "🤖 AI Xizmatlar", "🤖 AI Сервисы"}))
async def menu_ai_services(message: Message, state: FSMContext, bot: Bot, from_callback: bool = False, make_new: bool = False):
    # This handler handles both the Menu button and the "Check Subscription" callback loop if we adapt it
    
    if not from_callback:
        await cleanup_user_request(message, state, bot)
    
    user_id = message.from_user.id if hasattr(message, 'from_user') else message.chat.id
    
    async for session in get_session():
        lang = await get_user_language(user_id, session)
        
        is_subscribed = await check_subscription(bot, user_id, config.CHANNEL_ID)
        
        if is_subscribed:
            # 1. Send List
            await send_and_track(
                message, state, 
                text=texts.Texts.get("ai_services_list", lang)
            )
            # 2. Send Outro/Upsell
            await message.answer(
                text=texts.Texts.get("ai_services_outro", lang),
                reply_markup=keyboards.get_ai_services_upsell_keyboard(lang)
            )
        else:
            text = texts.Texts.get("ai_services_intro", lang)
            
            # Use a specific keyboard for AI check that might reuse the generic subscription check but redirects back here?
            # Or just use the generic get_subscription_keyboard which has callback "check_subscription"
            # But "check_subscription" handler (line 93) sends Lesson 1. We want it to send AI Services list.
            # So we typically need a different callback or smart handler.
            # Let's create a specific keyboard inline here for simplicity OR modify check_subscription to be context aware.
            # Context awareness is hard with stateless buttons.
            # So let's make a new callback button "check_subscription_ai"
            
            builder = keyboards.InlineKeyboardBuilder()
            builder.row(keyboards.InlineKeyboardButton(text=("📢 Kanalga o'tish" if lang == "uz" else "📢 Перейти в канал"), url=f"https://t.me/{config.CHANNEL_USERNAME.replace('@', '')}"))
            builder.row(keyboards.InlineKeyboardButton(text=("✅ Obuna bo'ldim" if lang == "uz" else "✅ Я подписался"), callback_data="check_subscription_ai"))
            
            await send_and_track(message, state, text, reply_markup=builder.as_markup())
