from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from keyboards.default.user import change_language_kb, languages, user_main_menu_keyboard_with_lang
from loader import _
from states.user import ChangeLanguageState
from utils.get_lang_code import get_lang_by_text

router = Router()


@router.message(F.text.in_(['Settings ⚙️', 'Настройки ⚙️', 'Sozlamalar ⚙️']))
async def menu_handler(message: types.Message, state: FSMContext):
    text = _("Siz sozlamalar menyusidasiz.")
    await message.answer(text=text, reply_markup=await change_language_kb())


@router.message(F.text.in_(["Tilni o'zgartirish 🌐", "Change language 🌐", "Изменить язык 🌐"]))
async def change_language_handler(message: types.Message, state: FSMContext):
    await message.answer(text=_("Tilingizni tanlang:"), reply_markup=languages)
    await state.set_state(ChangeLanguageState.language)


@router.message(StateFilter(ChangeLanguageState.language))
async def language_handler(message: types.Message, state: FSMContext):
    language = await get_lang_by_text(language=message.text)
    await state.update_data(language=language)
    await message.answer(text=_("Til muvaffaqiyatli o'zgartirildi.", locale=language),
                         reply_markup=await user_main_menu_keyboard_with_lang(language=language))
    await state.clear()
