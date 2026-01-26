from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_user(self, **kwargs) -> User:
        stmt = insert(User).values(**kwargs).returning(User)
        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.scalar_one()

    async def get_by_username(self, username: str) -> User | None:
        result = await self._session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_all_users(self) -> list[User]:
        result = await self._session.execute(select(User))
        return result.scalars().all()
