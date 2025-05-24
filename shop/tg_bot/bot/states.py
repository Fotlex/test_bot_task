from aiogram.fsm.state import State, StatesGroup


class Steps(StatesGroup):
    catalog_name = State()
    item_count = State()