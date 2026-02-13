from app.domain.entities.user_entity import UserEntity
from app.domain.interfaces.uow import IUnitOfWork


class UserService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def search_users(self, query: str, current_user_id: int) -> list[UserEntity]:
        async with self.uow:
            users = await self.uow.users.search_users(query=query)
            return [user for user in users if user.id != current_user_id]
