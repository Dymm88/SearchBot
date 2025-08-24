import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from db import init_db, async_session
from middlewares import DbSessionMiddleware
from routers.main import router as main_router


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    dp.message.middleware(DbSessionMiddleware(async_session))
    dp.include_router(main_router)
    
    await init_db()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
