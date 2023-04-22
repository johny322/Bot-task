# файл со стейтами
from aiogram.dispatcher.fsm.state import StatesGroup, State


class PollStatesGroup(StatesGroup):
    title = State()
    chat_id = State()
    answers = State()
    confirm = State()


class WeatherStatesGroup(StatesGroup):
    city = State()


class CurrencyStatesGroup(StatesGroup):
    from_currency = State()
    to_currency = State()
    amount = State()
