from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_user(self, user_id):
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    async def get_all_users(self):
        result = await self.session.execute(select(User))
        return result.scalars().all()
    
    async def add_user(
            self,
            user_id: int,
            username: str | None,
            first_name: str | None,
            last_name: str | None,
    ):
        user = User(
            id=int(user_id),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        self.session.add(user)
        await self.session.commit()
