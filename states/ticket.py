from aiogram.dispatcher.filters.state import StatesGroup, State


class Ticket(StatesGroup):
    add = State()