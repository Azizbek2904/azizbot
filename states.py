"""
FSM (Finite State Machine) holatlari.
Admin va user uchun ko'p qadamli amallar.
"""
from aiogram.fsm.state import State, StatesGroup


class AdCreation(StatesGroup):
    """Reklama yaratish bosqichlari"""
    waiting_photo = State()
    waiting_title = State()
    waiting_description = State()
    waiting_promo_text = State()
    waiting_link_type = State()
    waiting_link_url = State()
    waiting_button_text = State()
    confirm = State()


class ContestCreation(StatesGroup):
    """Konkurs yaratish bosqichlari"""
    waiting_title = State()
    waiting_description = State()
    waiting_photo = State()
    waiting_type = State()
    waiting_prizes = State()
    waiting_required_refs = State()
    waiting_end_date = State()
    confirm = State()


class ChannelAdd(StatesGroup):
    """Kanal qo'shish"""
    waiting_channel = State()
    waiting_mandatory = State()


class Broadcast(StatesGroup):
    """Ommaviy xabar"""
    waiting_message = State()
    confirm = State()


class UserSearch(StatesGroup):
    """User qidirish"""
    waiting_query = State()


class AdEdit(StatesGroup):
    """Reklama tahrirlash"""
    waiting_field = State()
    waiting_value = State()
