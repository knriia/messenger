"""Репозиторий для работы с сущностью пользователя."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user_entity import UserEntity
from app.domain.interfaces.user_repo import IUserRepository
from app.infrastructure.postgres.mappers.user_mapper import UserMapper
from app.infrastructure.postgres.models.user import User


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_user(self, username: str, hashed_password: str) -> UserEntity:
        new_user = User(username=username, hashed_password=hashed_password)
        self._session.add(new_user)
        await self._session.flush()
        return UserMapper.to_domain(new_user)

    async def search_users(self, query: str, limit: int = 10) -> list[UserEntity]:
        stmt = select(User).where(User.username.ilike(f"%{query}%")).limit(limit=limit)
        result = await self._session.execute(stmt)
        return [UserMapper.to_domain(u) for u in result.scalars().all()]


    async def get_by_username(self, username: str) -> UserEntity | None:
        stmt = select(User).where(User.username == username)
        result = await self._session.execute(stmt)
        db_user = result.scalar_one_or_none()
        return UserMapper.to_domain(db_user) if db_user else None
