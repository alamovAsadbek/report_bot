from datetime import datetime, timedelta

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from keyboards.default.report_kb import report_date_kb
from keyboards.inline.user import number_of_reports_kb
from loader import _
from main.constants import ReportType
from states.user import ReportStateForIncome
from utils.db_commands.user import get_user_income_and_expense_reports
from keyboards.default.user import user_main_menu_keyboard
from utils.main_functions import create_report

router = Router()


@router.message(F.text.in_(["Daromad bo'yicha hisobot📊", "Отчет о прибылях и убытках📊", "Income statement📊"]))
async def branches_handler(message: types.Message, state: FSMContext):
    await message.answer(_("Hisobot davomiyligini tanlang 😊 "), reply_markup=await report_date_kb())

    await state.set_state(ReportStateForIncome.waiting_for_report_date)


@router.message(StateFilter(ReportStateForIncome.waiting_for_report_date))
async def choose_income_filter_date(message: types.Message, state: FSMContext):
    user_text = message.text
    filter_date = None
    if user_text == _("Hammasi 📅"):
        filter_date = None
    elif user_text == _("Oxirgi 3 oylik hisobot 📊"):
        filter_date = datetime.now().utcnow() - timedelta(days=93)
    elif user_text == _("Oxirgi 1 oylik hisobot 📊"):
        filter_date = datetime.now().utcnow() - timedelta(days=31)
    elif user_text == _("Oxirgi 1 haftalik hisobot 📊"):
        filter_date = datetime.now().utcnow() - timedelta(days=7)
    elif user_text == _("Oxirgi 1 kunlik hisobot 📊"):
        filter_date = datetime.now().utcnow() - timedelta(days=1)
    await state.update_data(filter_date=filter_date)
    all_incomes: any or list = await get_user_income_and_expense_reports(chat_id=message.chat.id,
                                                                         report_type=ReportType.income.value,
                                                                         filter_date=filter_date)
    if not all_incomes:
        await message.answer(_("Sizda daromad bo'yicha hisobot yo'q!"), reply_markup=await user_main_menu_keyboard())
        return
    await message.answer(_("Hisobot tayyorlanmoqda... ⏳"), reply_markup=await user_main_menu_keyboard())
    income_report = create_report(data=all_incomes)
    inline_buttons = await number_of_reports_kb(all_incomes)

    await message.reply(income_report['report_text'], parse_mode='HTML', reply_markup=inline_buttons)
    await state.clear()
