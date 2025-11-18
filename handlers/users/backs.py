from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.default.user import user_main_menu_keyboard_with_lang
from loader import _

router = Router()


@router.message(F.text.in_(['Orqaga qaytish ⬅️', 'Back ⬅️', 'Назад ⬅️']))
async def menu_handler(message: types.Message, state: FSMContext):
    text = "Siz sozlamalar menyusidasiz.."
    await message.answer(text=text, reply_markup=await user_main_menu_keyboard_with_lang('uz'))
    await state.clear()


@router.message(F.text.in_(['Bekor qilish ❌', 'Cancel ❌', 'Отменить ❌']))
async def menu_handler(message: types.Message, state: FSMContext):
    text = "Bekor qilindi 😉"
    await message.answer(text=text, reply_markup=await user_main_menu_keyboard_with_lang('uz'))
    await state.clear()


@router.callback_query(lambda c: c.data in ['cancel_pagination'])
async def cancel_pagination_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Siz asosiy menyuga qaytadiz.. ⬅️",
                                        reply_markup=await user_main_menu_keyboard_with_lang('uz'))
    await callback_query.answer()
    await state.clear()
