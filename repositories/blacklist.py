from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import BlackList


class BlacklistRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def add_blacklist(self, user_id: int, data: list[str]):
        companies = {
            'companies': data,
        }
        result = BlackList(
            user_id=user_id,
            companies=companies,
        )
        self.session.add(result)
        await self.session.commit()
        
    async def get_all(self, user_id: int):
        result = await self.session.execute(
            select(BlackList.companies).where(BlackList.usser_id == user_id)
        )
        companies = result.scalar_one_or_none()
        return companies.get('companies', [])
