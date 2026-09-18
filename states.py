from aiogram.fsm.state import State, StatesGroup

class RegistrationState(StatesGroup):
    full_name = State()
    age = State()

class AdminState(StatesGroup):
    add_channel_id = State()
    add_channel_link = State()
    delete_channel_id = State()
    add_anime_code = State()
    add_anime_video = State()
    broadcast_msg = State()
