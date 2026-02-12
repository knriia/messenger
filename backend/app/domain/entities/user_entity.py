from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class UserEntity:
    id: int
    username: str
    email: str
    created_at: datetime
