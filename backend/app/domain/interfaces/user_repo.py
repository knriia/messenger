from abc import ABC, abstractmethod

from app.domain.entities.user_entity import UserEntity


class IUserRepository(ABC):
    @abstractmethod
    async def create_user(self, username: str, hashed_password: str) -> UserEntity:
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> UserEntity | None:
        pass

    @abstractmethod
    async def search_users(self, query: str, limit: int = 10) -> list[UserEntity]:
        """Поиск пользователей по совпадению в username."""
        pass
