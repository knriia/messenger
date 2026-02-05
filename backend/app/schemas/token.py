"""Схемы JWT-токенов."""

from datetime import datetime

from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: str
    user_id: int
    exp: datetime | None = None


class Token(BaseModel):
    access_token: str
    token_type: str
