"""Схемы данных пользователей."""

from pydantic import BaseModel, ConfigDict, EmailStr

from app.domain.entities.user_entity import UserCreateEntity


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None

    def to_entity(self) -> UserCreateEntity:
        return UserCreateEntity(
            username=self.username,
            password=self.password,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
        )


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr | None
    model_config = ConfigDict(from_attributes=True)
