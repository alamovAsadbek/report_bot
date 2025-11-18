from aiogram import types, Router, F

from loader import _

router = Router()


@router.message(F.text.in_(["Contact ☎️", "Aloqa ☎️"]))
async def contact_handler(message: types.Message):
    text = _("📲 Aloqa markazi: 1174 or (71) 203-66-66")
    await message.answer(text=text)
