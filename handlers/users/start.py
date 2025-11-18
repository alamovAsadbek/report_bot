from aiogram import F
from aiogram import types, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboards.common import phone_number_share_keyboard
from keyboards.default.user import languages, user_main_menu_keyboard_with_lang
from keyboards.default.user import user_main_menu_keyboard
from loader import _
from states.user import RegisterState
from utils.db_commands.user import get_user, add_user
from utils.get_lang_code import get_lang_by_text

router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    await state.clear()

    user = await get_user(chat_id=message.chat.id)
    if user:
        text = "Xush kelibsiz 😊"
        await message.answer(text=text, reply_markup=await user_main_menu_keyboard_with_lang('uz'))
    else:
        text = _("Ism familiyangizni kiriting 👇", locale='uz')
        await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegisterState.full_name)


# @router.message(StateFilter(RegisterState.language))
# async def language_handler(message: types.Message, state: FSMContext):
#     language = await get_lang_by_text(language=message.text)
#     await state.update_data(language=language)
#
#     text = _("Ism familiyangizni kiriting 👇", locale=language)
#     await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
#     await state.set_state(RegisterState.full_name)


@router.message(StateFilter(RegisterState.full_name))
async def get_full_name_handler(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)

    data = await state.get_data()
    language = 'uz'

    text = "Iltimos, quyidagi tugma orqali telefon raqamingizni kiriting 👇"
    await message.answer(text=text, reply_markup=await phone_number_share_keyboard(language=language))
    await state.set_state(RegisterState.phone_number)


@router.message(StateFilter(RegisterState.phone_number), F.content_type == types.ContentType.CONTACT)
async def get_phone_number_handler(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.contact.phone_number)

    data = await state.get_data()
    language = data.get('language')
    new_user = await add_user(message=message, data=data)
    if new_user:
        text = "Siz roʻyxatdan oʻtdingiz ✅"
        await message.answer(text=text, reply_markup=await user_main_menu_keyboard_with_lang('uz'))
    else:
        text = _("Kechirasiz, keyinroq qayta urinib ko'ring 😔", locale=language)
        await message.answer(text=text)
    await state.clear()
