from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Token


class TokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def add_token(self, user_id: int, data: dict[str, str]):
        token = Token(
            user_id=user_id,
            access_token=data.get("access_token"),
            refresh_token=data.get("refresh_token"),
        )
        self.session.add(token)
        await self.session.commit()
    
    async def get_token_time(self, user_id: int):
        token = await self.session.execute(select(Token.create_or_update).where(Token.user_id == user_id))
        return token.scalar_one_or_none()
    
    async def get_token(self, user_id: int):
        result = await self.session.execute(
            select(Token.access_token).where(Token.user_id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_refresh_token(self, user_id: int):
        result = await self.session.execute(
            select(Token.refresh_token).where(Token.user_id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def update_token(self, user_id: int, data: dict[str, str]):
        await self.session.execute(
            update(Token)
            .where(Token.user_id == user_id)
            .values(
                access_token=data.get("access_token"),
                refresh_token=data.get("refresh_token"),
            )
        )
        await self.session.commit()
