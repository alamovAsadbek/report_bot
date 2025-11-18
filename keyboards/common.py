from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _


async def phone_number_share_keyboard(language: str):
    markup = ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton(text=_("Telefon raqamni ulashish ☎️", locale=language), request_contact=True)
        ]], resize_keyboard=True
    )
    return markup
