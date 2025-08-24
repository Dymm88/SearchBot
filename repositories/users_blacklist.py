from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import UserBlackList


class UserBlacklistRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def add_user(self, user_id: int):
        user = UserBlackList(
            user_id=user_id
        )
        self.session.add(user)
        await self.session.commit()
    
    async def get_all(self):
        result = await self.session.execute(select(UserBlackList.user_first_name))
        return result.scalars().all()
    
    async def remove_user(self, user_id: str):
        user = await self.session.get(UserBlackList, user_id)
        if user:
            await self.session.delete(user)
            await self.session.commit()
