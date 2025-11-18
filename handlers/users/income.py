from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.default.user import cancel_kb, user_main_menu_keyboard, user_main_menu_keyboard_with_lang
from keyboards.inline.user import save_income_kb
from loader import _
from main.constants import ReportType, ReportStatus
from states.user import IncomeAmountState, IncomeDescriptionState
from utils.db_commands.user import add_income_and_expense_reports
from utils.main_functions import change_amount_to_string

router = Router()


@router.message(F.text.in_(['Daromad 📊', 'Доход 📊', 'Income 📊']))
async def branches_handler(message: types.Message, state: FSMContext):
    await message.answer(
        text=_('Daromadni kiriting. Misol uchun: 100000. Faqat raqamlardan iborat bo\'lishi kerak!'),
        reply_markup=await cancel_kb())
    await state.set_state(IncomeAmountState.income_amount)


@router.message(StateFilter(IncomeAmountState.income_amount))
async def income_amount_handler(message: types.Message, state: FSMContext):
    amount = message.text
    if not amount.isdigit():
        await message.answer(text=_('Miqdori notog\'ri kiritilgan. Miqdori raqamlardan iborat bo\'lishi kerak!'),
                             reply_markup=await cancel_kb())
        return
    await state.update_data(amount=amount)
    await message.answer(text=_(
        "Qo\'shimcha malumot kiriting! 📝"),
        reply_markup=types.ForceReply(input_field_placeholder=_("Tavsifni kiriting..."))
    )
    await state.set_state(IncomeDescriptionState.income_description)


@router.message(StateFilter(IncomeDescriptionState.income_description))
async def income_kb_handler(message: types.Message, state: FSMContext):
    description = message.text
    if len(description) <= 2:
        await message.answer(
            text=_('Ma\'lumotlar notog\'ri kiritilgan. Iltimos, 5 ta belgidan kattaroq malumot kiriting!'),
            reply_markup=await cancel_kb())
        return
    data = await state.get_data()
    amount = int(data.get('amount'))
    await state.update_data(description=description)
    new_amount = change_amount_to_string(amount)
    text = _(f'<b>💸Miqdor:</b> {new_amount} so\'m\n\n<b>📝Tavsif:</b> {description}')
    await message.answer(text=text, parse_mode=ParseMode.HTML, reply_markup=await save_income_kb())


@router.callback_query(lambda c: c.data in ['save_income', 'cancel_income'])
async def process_save_cancel(callback_query: CallbackQuery, state: FSMContext):
    try:
        action = callback_query.data
        if action == 'save_income':
            data = await state.get_data()
            data['type'] = ReportType.income.value
            data['status'] = ReportStatus.activated.value
            new_income = await add_income_and_expense_reports(data=data, message=callback_query.message)
            if new_income:
                await callback_query.answer(text='Daromadingiz muvaffaqiyatli saqlandi! ✅')
            else:
                await callback_query.answer(text='Xatolik yuz berdi! Iltimos, bizda qayta urinib ko\'ring.')
        elif action == 'cancel_income':
            await callback_query.answer(text='Daromadingiz saqlanmadi. ❌')
        await callback_query.message.delete_reply_markup()
        await callback_query.message.answer(text="Siz asosiy menyudasiz !  ✅",
                                            reply_markup=await user_main_menu_keyboard_with_lang('uz'))
        await state.clear()
    except Exception as e:
        print(e)
        await callback_query.message.answer(text=_('Xatolik yuz berdi! Iltimos, bizda qayta urinib ko\'ring.'),
                                            reply_markup=await user_main_menu_keyboard_with_lang('uz'))
