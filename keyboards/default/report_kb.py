from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import _


async def report_main_kb():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Umumiy hisobot 📊"))

            ],
            [
                KeyboardButton(text=_("Daromad bo'yicha hisobot📊")),
                KeyboardButton(text=_("Xarajatlar bo'yicha hisobot📉 ")),
            ],
            [
                KeyboardButton(text=_("Bekor qilish ❌"))
            ]
        ], resize_keyboard=True
    )

    return markup


async def report_date_kb():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Hammasi 📅")),
            ],
            [
                KeyboardButton(text=_("Oxirgi 3 oylik hisobot 📊")),
                KeyboardButton(text=_("Oxirgi 1 oylik hisobot 📊"))
            ],
            [
                KeyboardButton(text=_("Oxirgi 1 haftalik hisobot 📊")),
                KeyboardButton(text=_("Oxirgi 1 kunlik hisobot 📊"))
            ],
            [
                KeyboardButton(text=_("Bekor qilish ❌"))
            ]
        ], resize_keyboard=True
    )

    return markup
