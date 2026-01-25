from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.schemas.user import UserCreate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_user(self, user_data: UserCreate) -> User:
        stmt = insert(User).values(**user_data.model_dump()).returning(User)
        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.scalar_one()

    async def get_by_username(self, username: str) -> User | None:
        result = await self._session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_all_users(self) -> list[User]:
        result = await self._session.execute(select(User))
        return result.scalars().all()
