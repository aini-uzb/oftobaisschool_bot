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

# ADMIN: Confirm Payment
@router.callback_query(F.data.startswith("confirm_pay_"))
async def process_confirm_payment(callback: CallbackQuery, bot: Bot):
    payment_id = int(callback.data.split("_")[-1])
    
    async for session in get_session():
        # Get payment record
        payment_result = await session.execute(
            select(Payment).where(Payment.id == payment_id)
        )
        payment = payment_result.scalar_one_or_none()
        
        if not payment:
            await callback.answer("❌ To'lov topilmadi", show_alert=True)
            return
        
        # Update payment status
        await session.execute(
            update(Payment).where(Payment.id == payment_id).values(status="confirmed")
        )
        
        # Update user payment status
        await session.execute(
            update(User).where(User.user_id == payment.user_id).values(
                payment_status="confirmed",
                seminar_payment_confirmed=True if payment.tariff == "SEMINAR" else False
            )
        )
        await session.commit()
        
        # Get user info
        user_result = await session.execute(
            select(User).where(User.user_id == payment.user_id)
        )
        user = user_result.scalar_one_or_none()
        
        if user:
            lang = user.language or "uz"
            
            # Send confirmation to user
            if payment.tariff in ["SEMINAR", "SEMINAR_ONLINE", "SEMINAR_OFFLINE"]:
                # Send warm invitation with group link
                invitation_text = texts.Texts.get("seminar_payment_confirmed", lang).format(
                    code=user.seminar_access_code or "UNKNOWN",
                    link=config.SEMINAR_GROUP_LINK
                )
                try:
                    await bot.send_message(
                        chat_id=payment.user_id,
                        text=invitation_text,
                        parse_mode="HTML",
                        disable_web_page_preview=False
                    )
                except Exception as e:
                    print(f"Failed to send confirmation to user {payment.user_id}: {e}")
            else:
                # Regular payment confirmation
                try:
                    await bot.send_message(
                        chat_id=payment.user_id,
                        text=texts.Texts.get("payment_confirmed_partial" if payment.type != "full" else "payment_confirmed_full", lang)
                    )
                except Exception as e:
                    print(f"Failed to send confirmation to user {payment.user_id}: {e}")
        
        # Update admin message
        await callback.message.edit_caption(
            caption=callback.message.caption + "\n\n✅ TASDIQLANDI",
            reply_markup=None
        )
        await callback.answer("✅ To'lov tasdiqlandi!")

# ADMIN: Reject Payment
@router.callback_query(F.data.startswith("reject_pay_"))
async def process_reject_payment(callback: CallbackQuery, bot: Bot):
    payment_id = int(callback.data.split("_")[-1])
    
    async for session in get_session():
        await session.execute(
            update(Payment).where(Payment.id == payment_id).values(status="rejected")
        )
        await session.commit()
        
        await callback.message.edit_caption(
            caption=callback.message.caption + "\n\n❌ BEKOR QILINDI",
            reply_markup=None
        )
        await callback.answer("❌ To'lov bekor qilindi")
