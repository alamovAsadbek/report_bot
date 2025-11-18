
from aiogram.fsm.state import StatesGroup, State

class AdminBroadcast(StatesGroup):
    waiting_for_message = State()
    waiting_for_confirm = State()
