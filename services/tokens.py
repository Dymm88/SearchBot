from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.tokens import TokenRepository


class TokenService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def add_tokens(self, user_id: int, data: dict):
        token = TokenRepository(self.session)
        await token.add_token(
            user_id=user_id,
            data=data,
        )
    
    async def check_token(self, user_id: int):
        token_time = TokenRepository(self.session)
        result = await token_time.get_token_time(user_id)
        if result is not None and ((datetime.now() - result) > timedelta(days=13)):
            await self.refresh_token()
    
    async def refresh_token(self):
        ...
