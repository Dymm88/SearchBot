from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.main import get_phone
from services.tokens import TokenService

router = Router()

@router.message(F.text == 'Получить токены')
async def get_tokens(message: Message, session: AsyncSession):
    await TokenService(session).create_tokens(message.from_user.id)
    tokens = await TokenService(session).get_token(message.from_user.id)
    if tokens:
        await message.answer(
            text='Токены получены',
        )
    else:
        await message.answer(
            text='Ошибка получения'
        )
        
@router.message(F.text == "Get tokens")
async def request_phone(message: Message):
    await message.answer(
        "Please send your phone number by pressing the button below:",
        reply_markup=get_phone()
    )

@router.message(F.contact)
async def process_contact(message: Message):
    phone = message.contact.phone_number
    await message.answer(f"Your phone number: {phone}")