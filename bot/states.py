from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    name = State()
    contact = State()


class UserHousStates(StatesGroup):
    room = State()
    zipcode = State()
    min_sum = State()
    max_sum = State()
