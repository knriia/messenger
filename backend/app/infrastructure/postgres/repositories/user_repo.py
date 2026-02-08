"""Репозиторий для работы с сущностью пользователя."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.postgres.models.user import User
from app.schemas.user import UserCreate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_user(self, user_data: UserCreate, hashed_password: str) -> User:
        user_dict = user_data.model_dump(exclude={'password'})
        user_dict['hashed_password'] = hashed_password
        new_user = User(**user_dict)
        self._session.add(new_user)
        try:
            await self._session.commit()
            await self._session.refresh(new_user)
            return new_user
        except Exception:
            await self._session.rollback()
            raise

    async def search_users(self, query: str, limit: int = 10) -> list[User]:
        stmt = select(User).where(User.username.ilike(f"{query}")).limit(limit=limit)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())


    async def get_by_username(self, username: str) -> User | None:
        result = await self._session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()
