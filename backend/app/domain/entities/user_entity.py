from dataclasses import asdict, dataclass
from datetime import datetime


@dataclass(frozen=True, kw_only=True)
class UserEntity:
    id: int
    username: str
    email: str
    created_at: datetime


@dataclass(frozen=True, kw_only=True)
class UserWithPasswordEntity(UserEntity):
    hashed_password: str


@dataclass(frozen=True, kw_only=True)
class UserCreateBaseEntity:
    username: str
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True, kw_only=True)
class UserCreateEntity(UserCreateBaseEntity):
    password: str


@dataclass(frozen=True, kw_only=True)
class UserStoreEntity(UserCreateBaseEntity):
    hashed_password: str
