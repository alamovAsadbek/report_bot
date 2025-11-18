from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def confirm_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Yuborish", callback_data="confirm_send"),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_send"),
        ]
    ])
    return keyboard
