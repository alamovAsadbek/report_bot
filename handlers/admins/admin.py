import time
import asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InputFile
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from sqlalchemy import select

from keyboards.default.user import user_main_menu_keyboard
from main.config import ADMINS
from main.database import database
from main.models import User  # ❗ to'g'ri import

router = Router()

class BroadcastState(StatesGroup):
    waiting_content = State()
    waiting_approval = State()

def is_admin(user_id: int) -> bool:
    return str(user_id) in ADMINS

def approval_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="✅ Yuborish"), KeyboardButton(text="❌ Bekor qilish")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

@router.message(Command("send"))
async def start_broadcast(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return await message.answer("⛔️ Sizda ruxsat yo'q.")
    await state.clear()
    await state.set_state(BroadcastState.waiting_content)
    await message.answer("📨 Yubormoqchi bo‘lgan xabaringizni yuboring (matn yoki rasm).")

@router.message(BroadcastState.waiting_content, F.content_type.in_(["text", "photo"]))
async def receive_content(message: Message, state: FSMContext):
    data = {}
    if message.photo:
        data["photo_id"] = message.photo[-1].file_id
        data["caption"] = message.caption or ""
    else:
        data["text"] = message.text

    await state.update_data(**data)
    await state.set_state(BroadcastState.waiting_approval)

    if "photo_id" in data:
        await message.answer_photo(
            photo=data["photo_id"],
            caption=data["caption"] + "\n\n⬇️ Quyidagi tugmalardan birini tanlang:",
            reply_markup=approval_keyboard()
        )
    else:
        await message.answer(
            data["text"] + "\n\n⬇️ Quyidagi tugmalardan birini tanlang:",
            reply_markup=approval_keyboard()
        )

@router.message(BroadcastState.waiting_approval, F.text.in_(["✅ Yuborish", "❌ Bekor qilish"]))
async def final_approval(message: Message, state: FSMContext, bot: Bot):
    if not is_admin(message.from_user.id):
        return await message.answer("⛔️ Sizda ruxsat yo'q.")

    if message.text == "❌ Bekor qilish":
        await state.clear()
        return await message.answer("❌ Xabar yuborish bekor qilindi.", reply_markup=ReplyKeyboardRemove())

    data = await state.get_data()
    await message.answer("🚀 Xabar yuborilmoqda...", reply_markup=ReplyKeyboardRemove())

    query = select(User)
    all_users = await database.fetch_all(query)

    sent = 0
    blocked = 0
    failed = 0

    async def send_to_user(user):
        nonlocal sent, blocked, failed
        try:
            telegram_id = user["chat_id"]
            if "photo_id" in data:
                await bot.send_photo(chat_id=telegram_id, photo=data["photo_id"], caption=data["caption"])
            else:
                await bot.send_message(chat_id=telegram_id, text=data["text"])
            sent += 1
        except Exception as e:
            if "bot was blocked" in str(e):
                blocked += 1
            else:
                failed += 1
            print(f"❌ Xatolik foydalanuvchi {user['chat_id']}: {e}")

    start_time = time.time()
    await asyncio.gather(*[send_to_user(user) for user in all_users])
    end_time = time.time()
    elapsed_time = end_time - start_time

    await message.answer(
        f"✅ Xabar yuborildi.\n\n"
        f"👤 Jami foydalanuvchilar: {len(all_users)}\n"
        f"📬 Yuborildi: {sent}\n"
        f"🚫 Bloklaganlar: {blocked}\n"
        f"❌ Boshqa xatoliklar: {failed}\n\n"
        f"⏱ Yuborish vaqti: {round(elapsed_time, 2)} soniya",
        reply_markup=await user_main_menu_keyboard()
    )

    await state.clear()
    return None

@router.message(Command("users"))
async def list_users(message: Message):
    if not is_admin(message.from_user.id):
        return await message.answer("⛔️ Sizda ruxsat yo'q.")

    query = select(User)
    all_users = await database.fetch_all(query)

    if not all_users:
        return await message.answer("👥 Foydalanuvchilar ro'yxati bo'sh.")

    text = "👥 Foydalanuvchilar ro'yxati:\n\n"
    for i, user in enumerate(all_users, start=1):
        text += f"{i}. {user['full_name']} - <code>{user['chat_id']}</code> - <code>{user['phone_number']}</code>\n"

    if len(text) >= 4000:
        with open("/tmp/users.txt", "w", encoding="utf-8") as f:
            for i, user in enumerate(all_users, start=1):
                f.write(f"{i}. {user['full_name']} - {user['chat_id']}\n")
        await message.answer_document(InputFile("/tmp/users.txt"))
    else:
        await message.answer(text)
