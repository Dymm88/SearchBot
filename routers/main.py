from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.main import main_keyboard
from services.tokens import TokenService
from services.users import UserService

router = Router()


@router.message(Command('start'))
async def start_handler(message: Message, session: AsyncSession):
    user = UserService(session)
    data = {
        'user_id': message.from_user.id,
        'username': message.from_user.username,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name,
    }
    await user.create_user(data)
    await TokenService(session).check_token(data['user_id'])
    await message.answer(
        text='Привет! Ты зарегистрирован в базе.',
        reply_markup=main_keyboard(data['user_id'])
    )
