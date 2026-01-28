from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy import update, select, func
from src import config, texts, keyboards
from src.database.db import get_session
from src.database.models import Payment, User
import asyncio

router = Router()

class BroadcastState(StatesGroup):
    waiting_for_message = State()
    waiting_for_confirm = State()

# --- BROADCAST HANDLERS ---
@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message, state: FSMContext):
    if message.from_user.id not in config.ADMIN_IDS:
        return
        
    await message.answer("📢 <b>Broadcast (Rassilka)</b>\n\nYubormoqchi bo'lgan xabaringizni yozing yoki forward qiling (Rasm, Video, Matn...)\n\nНапишите или перешлите сообщение, которое хотите отправить всем.")
    await state.set_state(BroadcastState.waiting_for_message)

@router.message(BroadcastState.waiting_for_message)
async def process_broadcast_message(message: Message, state: FSMContext):
    # Save the message ID and Chat ID to copy from
    await state.update_data(
        broadcast_msg_id=message.message_id,
        broadcast_chat_id=message.chat.id
    )
    
    # Check user count
    async for session in get_session():
        result = await session.execute(select(func.count(User.user_id)))
        count = result.scalar()
        
    await message.answer(
        f"📢 <b>Rassilka tayyor!</b>\n\nJami foydalanuvchilar: <b>{count} ta</b>\n\nShu xabarni hammaga yuboraymi?",
        reply_markup=keyboards.get_broadcast_confirm_keyboard()
    )
    # We copy the message back to admin to show preview
    await message.copy_to(chat_id=message.chat.id)
    
    await state.set_state(BroadcastState.waiting_for_confirm)

@router.callback_query(BroadcastState.waiting_for_confirm, F.data == "broadcast_cancel")
async def cancel_broadcast(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("❌ Rassilka bekor qilindi.")

@router.callback_query(BroadcastState.waiting_for_confirm, F.data == "broadcast_confirm")
async def execute_broadcast(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    msg_id = data.get("broadcast_msg_id")
    from_chat_id = data.get("broadcast_chat_id")
    
    await callback.message.edit_text("⏳ Rassilka boshlandi... (Bu biroz vaqt olishi mumkin)")
    
    sent_count = 0
    blocked_count = 0
    
    async for session in get_session():
        result = await session.execute(select(User.user_id))
        users = result.scalars().all()
        
    for user_id in users:
        try:
            await bot.copy_message(chat_id=user_id, from_chat_id=from_chat_id, message_id=msg_id)
            sent_count += 1
            await asyncio.sleep(0.05) # Avoid flood limits
        except Exception as e:
            blocked_count += 1
            
    await callback.message.answer(
        f"✅ <b>Rassilka tugadi!</b>\n\n"
        f"📨 Yuborildi: {sent_count}\n"
        f"🚫 Bloklanganlar (yoki xato): {blocked_count}"
    )
    await state.clear()
# --------------------------

@router.callback_query(F.data.startswith("admin_confirm_"))
async def process_admin_confirm(callback: CallbackQuery, bot: Bot):
    payment_id = int(callback.data.split("_")[-1])
    
    async for session in get_session():
        # Update Payment
        await session.execute(
            update(Payment).where(Payment.id == payment_id).values(status="confirmed")
        )
        
        # Get Payment details to update User
        result = await session.execute(select(Payment).where(Payment.id == payment_id))
        payment = result.scalar_one()
        
        # Update User
        payment_status = "full" if payment.type == "full" else "partial"
        await session.execute(
            update(User).where(User.user_id == payment.user_id).values(
                payment_status=payment_status,
                payment_date=payment.created_at # approximate
            )
        )
        await session.commit()
        
        # Notify User
        try:
            # We don't know user language here easily without querying. For now default to UZ or try to query.
            # Ideally fetch language from User table.
            result_user_lang = await session.execute(select(User.language).where(User.user_id == payment.user_id))
            user_lang = result_user_lang.scalar_one_or_none() or "uz"

            # Determine key based on payment type
            # payment.type can be "full", "partial_1", "partial_2" (though we only implemented partial_1 for now in flow)
            if payment.type in ["full"]:
                msg_key = "payment_confirmed_full"
            else:
                msg_key = "payment_confirmed_partial"

            await bot.send_message(
                chat_id=payment.user_id,
                text=texts.Texts.get(msg_key, user_lang)
            )
        except Exception as e:
            await callback.answer(f"Failed to notify user: {e}", show_alert=True)

    await callback.message.edit_caption(
        caption=callback.message.caption + "\n\n✅ ТАСДИҚЛАНДИ",
        reply_markup=None
    )

@router.callback_query(F.data.startswith("admin_reject_"))
async def process_admin_reject(callback: CallbackQuery):
    payment_id = int(callback.data.split("_")[-1])
    
    async for session in get_session():
        await session.execute(
            update(Payment).where(Payment.id == payment_id).values(status="rejected")
        )
        await session.commit()
    
    await callback.message.edit_caption(
        caption=callback.message.caption + "\n\n❌ РАД ЭТИЛДИ",
        reply_markup=None
    )
