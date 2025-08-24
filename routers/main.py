from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.main import main_keyboard, get_tokens
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
    token = await TokenService(session).get_token(data['user_id'])
    if token is None:
        await message.answer(
            text='Привет! Для начала необходимо получить токены от HeadHunter.',
            reply_markup=get_tokens()
        )
    else:
        await TokenService(session).check_token(data['user_id'])
        await message.answer(
            text='Привет! Ты зарегистрирован в базе.',
            reply_markup=main_keyboard(data['user_id'])
        )
