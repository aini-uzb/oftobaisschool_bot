from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy import update, select
from src import config, texts, keyboards
from src.database.db import get_session
from src.database.models import User, Payment
import string
import random

router = Router()

class PaymentState(StatesGroup):
    waiting_for_receipt = State()

async def generate_seminar_code(session) -> str:
    """Generate unique seminar access code in format SEM-XXXX"""
    while True:
        # Generate 4 random alphanumeric characters
        chars = string.ascii_uppercase + string.digits
        code_suffix = ''.join(random.choices(chars, k=4))
        code = f"SEM-{code_suffix}"
        
        # Check if code already exists
        result = await session.execute(
            select(User).where(User.seminar_access_code == code)
        )
        existing = result.scalar_one_or_none()
        
        if not existing:
            return code

async def get_user_language(user_id: int, session) -> str:
    result = await session.execute(select(User.language).where(User.user_id == user_id))
    lang = result.scalar_one_or_none()
    return lang or "uz"

@router.callback_query(F.data == "show_tariffs")
async def process_show_tariffs(callback: CallbackQuery):
    async for session in get_session():
        lang = await get_user_language(callback.from_user.id, session)
        await callback.message.edit_text(texts.Texts.get("tariffs_desc", lang), reply_markup=keyboards.get_tariffs_keyboard(lang))

# --- SELECT TARIFF ---

@router.callback_query(F.data == "select_pro")
async def process_select_pro(callback: CallbackQuery):
    async for session in get_session():
        lang = await get_user_language(callback.from_user.id, session)
        await callback.message.edit_text(texts.Texts.get("selected_tariff_pro", lang), reply_markup=keyboards.get_pro_payment_options_keyboard(lang))

@router.callback_query(F.data.in_({"select_lite", "select_vip"}))
async def process_select_other(callback: CallbackQuery):
    async for session in get_session():
        lang = await get_user_language(callback.from_user.id, session)
        tariff = callback.data.split("_")[1].upper() # LITE or VIP
        
        # We need a text key for selected tariff. For now reuse generic or create one.
        # But wait, we need to show OPTIONS.
        if tariff == "LITE":
             await callback.message.edit_text(texts.Texts.get("tariffs_desc", lang), reply_markup=keyboards.get_lite_payment_options_keyboard(lang))
        elif tariff == "VIP":
             await callback.message.edit_text(texts.Texts.get("tariffs_desc", lang), reply_markup=keyboards.get_vip_payment_options_keyboard(lang))

# --- PAYMENT INSTRUCTIONS ---

@router.callback_query(F.data == "pay_pro_full")
async def process_pay_pro_full(callback: CallbackQuery, state: FSMContext):
    try:
        await state.set_state(PaymentState.waiting_for_receipt)
        async for session in get_session():
            lang = await get_user_language(callback.from_user.id, session)
            print(f"DEBUG: pay_pro_full triggered for {callback.from_user.id}")
            
            await state.update_data(
                tariff="PRO",
                amount=config.PRICES['PRO']['full'],
                type="full",
                lang=lang,
                payment_instruction_msg_id=callback.message.message_id
            )
            
            type_text = "Тўлиқ" if lang == "uz" else "Полная оплата"
            text = texts.Texts.get("payment_instructions", lang).format(tariff="PRO", type=type_text, amount=f"{config.PRICES['PRO']['full']:,}".replace(",", " "))
            await callback.message.edit_text(text, reply_markup=keyboards.get_payment_back_keyboard("pro", lang))
    except Exception as e:
        import traceback
        err = traceback.format_exc()
        print(f"CRITICAL ERROR in pay_pro_full: {err}")
        await callback.answer(f"❌ ERROR: {str(e)[:180]}", show_alert=True)

@router.callback_query(F.data == "pay_lite_full")
async def process_pay_lite_full(callback: CallbackQuery, state: FSMContext):
    try:
        await state.set_state(PaymentState.waiting_for_receipt)
        async for session in get_session():
            lang = await get_user_language(callback.from_user.id, session)
            
            await state.update_data(
                tariff="LITE",
                amount=config.PRICES['LITE']['full'],
                type="full",
                lang=lang,
                payment_instruction_msg_id=callback.message.message_id
            )
            
            type_text = "Тўлиқ" if lang == "uz" else "Полная оплата"
            text = texts.Texts.get("payment_instructions", lang).format(tariff="LITE", type=type_text, amount=f"{config.PRICES['LITE']['full']:,}".replace(",", " "))
            await callback.message.edit_text(text, reply_markup=keyboards.get_payment_back_keyboard("pro", lang))
    except Exception as e:
        import traceback
        err = traceback.format_exc()
        print(f"CRITICAL ERROR in pay_lite_full: {err}")
        await callback.answer(f"❌ ERROR: {str(e)[:180]}", show_alert=True)

@router.callback_query(F.data == "pay_lite_half")
async def process_pay_lite_half(callback: CallbackQuery, state: FSMContext):
    try:
        await state.set_state(PaymentState.waiting_for_receipt)
        async for session in get_session():
            lang = await get_user_language(callback.from_user.id, session)
            
            await state.update_data(
                tariff="LITE",
                amount=config.PRICES['LITE']['half'],
                type="partial_1",
                lang=lang,
                payment_instruction_msg_id=callback.message.message_id
            )
            
            type_text = "Bo'lib tolash 1-qism" if lang == "uz" else "Рассрочка 1-часть"
            text = texts.Texts.get("payment_instructions", lang).format(tariff="LITE", type=type_text, amount=f"{config.PRICES['LITE']['half']:,}".replace(",", " "))
            await callback.message.edit_text(text, reply_markup=keyboards.get_payment_back_keyboard("pro", lang))
    except Exception as e:
        import traceback
        err = traceback.format_exc()
        print(f"CRITICAL ERROR in pay_lite_half: {err}")
        await callback.answer(f"❌ ERROR: {str(e)[:180]}", show_alert=True)

@router.callback_query(F.data == "pay_vip_full")
async def process_pay_vip_full(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PaymentState.waiting_for_receipt)
    async for session in get_session():
        lang = await get_user_language(callback.from_user.id, session)
        
        await state.update_data(
            tariff="VIP",
            amount=config.PRICES['VIP']['full'],
            type="full",
            lang=lang,
            payment_instruction_msg_id=callback.message.message_id
        )
        
        type_text = "Тўлиқ" if lang == "uz" else "Полная оплата"
        text = texts.Texts.get("payment_instructions", lang).format(tariff="VIP", type=type_text, amount=f"{config.PRICES['VIP']['full']:,}".replace(",", " "))
        await callback.message.edit_text(text, reply_markup=keyboards.get_payment_back_keyboard("pro", lang))

@router.callback_query(F.data == "pay_vip_half")
async def process_pay_vip_half(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PaymentState.waiting_for_receipt)
    async for session in get_session():
        lang = await get_user_language(callback.from_user.id, session)
        
        await state.update_data(
            tariff="VIP",
            amount=config.PRICES['VIP']['half'],
            type="partial_1", # Using same partial logic
            lang=lang,
            payment_instruction_msg_id=callback.message.message_id
        )
        
        type_text = "Брон (50%)" if lang == "uz" else "Бронь (50%)"
        text = texts.Texts.get("payment_instructions", lang).format(tariff="VIP", type=type_text, amount=f"{config.PRICES['VIP']['half']:,}".replace(",", " "))
        await callback.message.edit_text(text, reply_markup=keyboards.get_payment_back_keyboard("pro", lang))

@router.callback_query(F.data == "pay_pro_half")
async def process_pay_pro_half(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PaymentState.waiting_for_receipt)
    async for session in get_session():
        lang = await get_user_language(callback.from_user.id, session)
        
        await state.update_data(
            tariff="PRO",
            amount=config.PRICES['PRO']['half'],
            type="partial_1",
            lang=lang,
            payment_instruction_msg_id=callback.message.message_id
        )
        
        type_text = "Bo'lib tolash 1-qism" if lang == "uz" else "Рассрочка 1-часть"
        text = texts.Texts.get("payment_instructions", lang).format(tariff="PRO", type=type_text, amount=f"{config.PRICES['PRO']['half']:,}".replace(",", " "))
        await callback.message.edit_text(text, reply_markup=keyboards.get_payment_back_keyboard("pro", lang))

# --- HANDLE RECEIPT ---

@router.message(PaymentState.waiting_for_receipt, F.photo)
async def process_receipt_upload(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    tariff = data.get("tariff")
    amount = data.get("amount")
    p_type = data.get("type")
    lang = data.get("lang", "uz")
    instruction_msg_id = data.get("payment_instruction_msg_id")

    # Delete instruction message
    if instruction_msg_id:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=instruction_msg_id)
        except:
            pass
    
    # Save receipt info to DB
    async for session in get_session():
        # Create Payment Record
        payment = Payment(
            user_id=message.from_user.id,
            tariff=tariff,
            amount=amount,
            type=p_type,
            status="pending",
            receipt_photo=message.photo[-1].file_id 
        )
        session.add(payment)
        
        #Generate seminar code if SEMINAR tariff
        seminar_code = None
        if tariff == "SEMINAR":
            seminar_code = await generate_seminar_code(session)
        
        # Update User Tariff selection
        update_values = {
            "tariff": tariff,
            "payment_status": "pending_check"
        }
        if seminar_code:
            update_values["seminar_access_code"] = seminar_code
            
        await session.execute(
            update(User).where(User.user_id == message.from_user.id).values(**update_values)
        )
        await session.commit()
        await session.refresh(payment)
        
    # Notify Admin (Admin language is likely irrelevant mostly, or defaults)
        admin_text = (
            f"🆕 ЯНГИ ТЎЛОВ / NEW PAYMENT!\n\n"
            f"👤 User: {message.from_user.full_name} (@{message.from_user.username})\n"
            f"🆔 ID: {message.from_user.id}\n"
            f"💰 Tariff: {tariff} ({p_type})\n"
            f"💵 Summa: {amount:,}".replace(",", " ")
        )
        
        if seminar_code:
            admin_text += f"\n\n🎫 КОД ДОСТУПА: <code>{seminar_code}</code>"
        
        
        try:
             # Notify all admins
            for admin_id in config.ADMIN_IDS:
                try:
                    await bot.send_photo(
                        chat_id=admin_id,
                        photo=message.photo[-1].file_id,
                        caption=admin_text,
                        reply_markup=keyboards.get_admin_payment_keyboard(payment.id)
                    )
                except Exception as ex:
                     print(f"Failed to notify admin {admin_id}: {ex}")
        except Exception as e:
            print(f"Failed to notify admins: {e}")

    await state.clear()
    
    if tariff == "SEMINAR":
        await message.answer(texts.Texts.get("seminar_receipt_received", lang).format(code=seminar_code or "UNKNOWN"))
    else:
        await message.answer(texts.Texts.get("receipt_accepted", lang))
