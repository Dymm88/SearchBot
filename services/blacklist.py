import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession

from config import APPLICATION, EMAIL
from repositories.blacklist import BlacklistRepository
from services.tokens import TokenService


class BlacklistService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def add_in_blacklist(self, vacancy_list: list[str], user_id: int):
        blacklist = BlacklistRepository(self.session)
        companies = await blacklist.get_all(user_id)
        async with aiohttp.ClientSession() as session:
            for name in vacancy_list:
                if name['employer']['name'] in companies:
                    url = f"https://api.hh.ru/vacancies/blacklisted/{name['id']}"
                    async with session.put(
                            url=url,
                            headers={
                                "Authorization": f"Bearer {await TokenService(self.session).get_token(user_id)}",
                                "User-Agent": f"{APPLICATION} ({EMAIL})",
                                "Content-Type": "application/json",
                            }
                    
                    ) as resp:
                        if resp.status != 200:
                            print(f"Error {resp.status} for vacancy {name['id']}")
    
    async def get_black_list(self, user_id: int):
        url = "https://api.hh.ru/vacancies/blacklisted"
        headers = {
            "Authorization": f"Bearer {await TokenService(self.session).get_token(user_id)}",
            "User-Agent": f"{APPLICATION} ({EMAIL})",
            "Content-Type": "application/json",
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=headers) as resp:
                blacklist_data = await resp.json()
                blacklist = [
                    t['id'] for t in blacklist_data['items']
                ]
                return blacklist
    
    async def add_companies(self, user_id: int, companies: list[str]):
        await BlacklistRepository(self.session).add_blacklist(user_id, companies)
