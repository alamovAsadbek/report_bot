from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from loader import _


async def user_main_menu_keyboard_with_lang(language: str):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Daromad 📊", locale=language)),
                KeyboardButton(text=_("Xarajat 📉", locale=language)),
            ],
            [
                KeyboardButton(text=_("Hisobotlar 📄", locale=language)),
            ],
            # [
            #     KeyboardButton(text=_("Admin bilan aloqa ☎️", locale=language)),
            #     KeyboardButton(text=_("Sozlanmalar ⚙️", locale=language)),
            # ]
        ], resize_keyboard=True
    )

    return markup


async def user_main_menu_keyboard():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Daromad 📊")),
                KeyboardButton(text=_("Xarajat 📉"))
            ],
            [

                KeyboardButton(text=_("Hisobotlar 📄")),
            ],
            # [
            #     KeyboardButton(text=_("Admin bilan aloqa ☎️")),
            #     KeyboardButton(text=_("Sozlanmalar ⚙️")),
            # ]
        ], resize_keyboard=True
    )

    return markup


languages = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Uzbek 🇺🇿"),
            KeyboardButton(text="Russian 🇷🇺"),
            KeyboardButton(text="English 🇺🇸"),
        ]
    ], resize_keyboard=True
)


async def income_edit_kb():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("Ortga qaytish ⬅️"), callback_data="back_to_income_menu")],
        ]
    )
    return markup


async def inside_menu_kb():
    markup = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text=_("Yetkazib berish")),
            KeyboardButton(text=_("Olib ketish")),
        ],
        [
            KeyboardButton(text=_("Orqaga"))
        ]
    ])
    return markup


async def inside_deliver_kb():
    markup = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text=_("Joylashuvingizni yuboring"))
        ],
        [
            KeyboardButton(text=_("Mening barcha joylarim"))
        ]
    ], resize_keyboard=True)
    return markup


async def change_language_kb():
    markup = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text=_("Tilni o'zgartirish 🌐"))
        ],
        [
            KeyboardButton(text=_("Orqaga ⬅️"))
        ]
    ], resize_keyboard=True)
    return markup


async def submit_benefit_kb():
    markup = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text=_("Saqlash ✅"))
        ],
        [
            KeyboardButton(text=_("Orqaga ⬅️"))
        ]
    ], resize_keyboard=True)
    return markup


async def cancel_kb():
    markup = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text=_("Bekor qilish ❌"))
        ]
    ], resize_keyboard=True)
    return markup
