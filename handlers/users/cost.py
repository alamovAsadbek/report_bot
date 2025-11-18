from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.default.user import cancel_kb, user_main_menu_keyboard_with_lang
from keyboards.inline.user import save_cost_kb
from loader import _
from main.constants import ReportType, ReportStatus
from states.user import CostAmountState, CostDescriptionState
from utils.db_commands.user import add_income_and_expense_reports
from utils.main_functions import change_amount_to_string

router = Router()


@router.message(F.text.in_(['Xarajat 📉', 'Cost 📉', 'Стоимость 📉']))
async def branches_handler(message: types.Message, state: FSMContext):
    await message.answer(
        text='Xarajatingizni kiriting. Misol uchun: 100000. Faqat raqamlardan iborat bo\'lishi kerak!',
        reply_markup=await cancel_kb())
    await state.set_state(CostAmountState.cost_amount)


@router.message(StateFilter(CostAmountState.cost_amount))
async def cost_amount_handler(message: types.Message, state: FSMContext):
    amount = message.text
    if not amount.isnumeric():
        await message.answer(text='Miqdori notog\'ri kiritilgan. Miqdorni to\'g\'ri kiriting.',
                             reply_markup=await cancel_kb())
        return
    await state.update_data(amount=amount)
    await message.answer(text="Qo\'shimcha malumot kiriting! 📝",
                         reply_markup=types.ForceReply(input_field_placeholder="Tavsifni kiriting...")
                         )
    await state.set_state(CostDescriptionState.cost_description)


@router.message(StateFilter(CostDescriptionState.cost_description))
async def cost_kb_handler(message: types.Message, state: FSMContext):
    description = message.text
    if len(description) < 5:
        await message.answer(
            text='Ma\'lumotlar notog\'ri kiritilgan. Iltimos, 5 ta belgidan kattaroq malumot kiriting!',
            reply_markup=await cancel_kb())
        return
    data = await state.get_data()
    amount = int(data.get('amount'))
    await state.update_data(description=description)
    new_amount = change_amount_to_string(amount)
    text = f'<b>💸Miqdor:</b> {str(new_amount)} so\'m\n\n<b>📝Tavsif:</b> {description}'
    await message.answer(text=text, parse_mode=ParseMode.HTML, reply_markup=await save_cost_kb())


@router.callback_query(lambda c: c.data in ['save_cost', 'cancel_cost'])
async def process_save_cancel(callback_query: CallbackQuery, state: FSMContext):
    try:
        action = callback_query.data
        if action == 'save_cost':
            data = await state.get_data()
            data['type'] = ReportType.expense.value
            data['status'] = ReportStatus.activated.value
            new_cost = await add_income_and_expense_reports(data=data, message=callback_query.message)
            if new_cost:
                await callback_query.answer(text='Xarajat muvaffaqiyatli saqlandi! ✅')
            else:
                await callback_query.answer(text='Xatolik yuz berdi! Iltimos, bizda qayta urinib ko\'ring.')
        elif action == 'cancel_cost ':
            await callback_query.answer('Xarajat saqlanmadi. ❌')
        await callback_query.message.delete_reply_markup()
        await callback_query.message.answer(text="Siz asosiy menyudasiz !",
                                            reply_markup=await user_main_menu_keyboard_with_lang('uz'))
        await state.clear()
    except Exception as error:
        print(error)
        await callback_query.message.answer(text='Xatolik yuz berdi! Iltimos, bizda qayta urinib ko\'ring.')
