from aiogram import Router

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from keyboards.default.user import user_main_menu_keyboard, user_main_menu_keyboard_with_lang
from keyboards.inline.user import delete_report_kb
from loader import _

from utils.db_commands.user import get_one_report, update_status_report
from utils.main_functions import change_amount_to_string

router = Router()


@router.callback_query(lambda c: c.data.startswith("report_page_"))
async def delete_report_handler(callback_query: CallbackQuery, state: FSMContext):
    """
    This handler is called when the user clicks on the "Delete" button in the report page.
    It fetches the report details and asks for confirmation to delete it.
    :param callback_query: CallbackQuery, the callback query that was clicked.
    :param state: FSMContext
    :return: None
    """
    await callback_query.answer()

    # Extract the report ID from the callback data
    report_id = int(callback_query.data.split("_")[2])

    # Fetch the report details
    report = await get_one_report(report_id)

    if report is None:
        await callback_query.message.answer("Report not found.",
                                            reply_markup=await user_main_menu_keyboard_with_lang('uz'))
        return

    # Format the amount properly
    new_amount = change_amount_to_string(int(report.get('amount')))

    # Prepare the confirmation message
    text = _(
        f'<b>Hisobotni o\'chirmoqchimisiz?</b>\n\n'
        f'<b>💸 Miqdor:</b> {str(new_amount)} so\'m\n\n'
        f'<b>📝 Tavsif:</b> {report.get("description")}'
    )

    # Send confirmation message with the delete options
    await callback_query.message.answer(text=text, parse_mode='HTML', reply_markup=await delete_report_kb())

    # Save the report ID in the state, so we can access it later
    await state.update_data(report_id=report_id)


@router.callback_query(lambda c: c.data == "delete_report")
async def confirm_delete_report(callback_query: CallbackQuery, state: FSMContext):
    """
    This handler is called when the user confirms the report deletion.
    It deletes the report from the database and sends a confirmation message.
    :param callback_query: CallbackQuery, the callback query that was clicked.
    :param state: FSMContext
    :return: None
    """
    await callback_query.answer()
    # Retrieve the report ID from the state
    user_data = await state.get_data()
    report_id = user_data.get('report_id')
    # If no report ID exists, return an error (this should not happen)
    if report_id is None:
        await callback_query.message.answer("No report ID found.",
                                            reply_markup=await user_main_menu_keyboard_with_lang('uz'))
        await state.clear()
        return

    # Delete the report from the database
    success = await update_status_report(report_id)
    if success:
        # Send a confirmation message to the user
        await callback_query.message.answer(
            f"Hisobot o'chirildi. ✅",
            reply_markup=await user_main_menu_keyboard_with_lang('uz')
        )
    else:
        await callback_query.message.answer(
            "Xatolik yuz berdi. Hisobotni o'chirib bo'lmadi. ❌",
            reply_markup=await user_main_menu_keyboard_with_lang('uz')
        )

    # Clear the state after the operation
    await state.clear()


@router.callback_query(lambda c: c.data == "back_to_main_menu")
async def back_to_main_menu(callback_query: CallbackQuery, state: FSMContext):
    """
    This handler is called when the user presses the "Back to Main Menu" button.
    It sends the user back to the main menu.
    :param callback_query: CallbackQuery, the callback query that was clicked.
    :param state: FSMContext
    :return: None
    """
    await callback_query.answer()
    await callback_query.message.answer(
        "Orqaga qaytildi. 🔙", reply_markup=await user_main_menu_keyboard('uz')
    )
    await state.clear()
