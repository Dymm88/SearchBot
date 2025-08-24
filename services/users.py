from sqlalchemy.ext.asyncio import AsyncSession

from repositories.users import UserRepository


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_user(self, user_id):
        user = UserRepository(self.session)
        return await user.get_user(user_id)
    
    async def create_user(self, user_data):
        user = UserRepository(self.session)
        check_user = await user.get_user(user_data['user_id'])
        if not check_user:
            await user.add_user(
                user_id=user_data['user_id'],
                username=user_data['username'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
            )
    
    async def get_all_users(self):
        user = UserRepository(self.session)
        return await user.get_all_users()
