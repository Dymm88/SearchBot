from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Token


class TokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def add_token(self,user_id: int, data: dict[str, str]):
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

