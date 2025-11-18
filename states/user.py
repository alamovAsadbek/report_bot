from aiogram.fsm.state import StatesGroup, State


class RegisterState(StatesGroup):
    """
    This state is used to store the user's information while registering.
    """
    language = State()
    full_name = State()
    phone_number = State()


class ChangeLanguageState(StatesGroup):
    """
    This state is used to store the language selected by the user.
    """
    language = State()


class FeedbackState(StatesGroup):
    """
    This state is used to store the feedback message sent by the user.
    """
    get_feedback = State()


class IncomeAmountState(StatesGroup):
    """
    This state is used to store the benefits amount selected by the user.
    """
    income_amount = State()


class IncomeDescriptionState(StatesGroup):
    """
    This state is used to store the benefits description selected by the user.
    """
    income_description = State()


class CostAmountState(StatesGroup):
    """
    This state is used to store the expenses amount selected by the user.
    """
    cost_amount = State()


class CostDescriptionState(StatesGroup):
    """
    This state is used to store the expenses description selected by the user.
    """
    cost_description = State()


class ReportStateForCost(StatesGroup):
    """
    This state is used to store the report message sent by the user.
    """
    waiting_for_report_date = State()


class ReportStateForIncome(StatesGroup):
    """
    This state is used to store the report message sent by the user.
    """
    waiting_for_report_date = State()


class GlobalReportState(StatesGroup):
    """
    This state is used to store the global report message sent by the user.
    """
    waiting_for_report_date = State()
