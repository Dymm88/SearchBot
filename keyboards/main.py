from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from config import ADMINS


def main_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    
    if str(user_id) in ADMINS:
        builder.button(text='Инфо')
        builder.button(text='Админка')
    else:
        builder.button(text='Инфо')
        builder.button(text='Поиск вакансий')
    
    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
    )


def get_tokens() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    
    builder.button(text='Получить токены')
    
    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
    )

def get_phone() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    
    builder.button(
        text="Отправить номер телефона",
        request_contact=True
    )
    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
    )

