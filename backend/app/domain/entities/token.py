from dataclasses import dataclass


@dataclass(frozen=True)
class TokenEntity:
    username: str
    user_id: int
    exp: int | None = None
