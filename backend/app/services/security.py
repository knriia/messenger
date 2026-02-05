"""Сервис обеспечения безопасности и аутентификации."""

import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from datetime import datetime, timedelta, timezone

from app.core.config import Settings
from app.schemas.token import TokenPayload


class SecurityService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.password_hash = PasswordHash((Argon2Hasher(),))

    def hash_password(self, password: str) -> str:
        return self.password_hash.hash(password=password)


    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.password_hash.verify(plain_password, hashed_password)


    def create_access_token(self, payload: TokenPayload) -> str:
        payload.exp = datetime.now(timezone.utc) + timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return jwt.encode(payload.model_dump(), self.settings.SECRET_KEY, algorithm=self.settings.ALGORITHM)

    def decode_token(self, token: str) -> TokenPayload | None:
        try:
            payload_dict = jwt.decode(
                token,
                self.settings.SECRET_KEY,
                algorithms=[self.settings.ALGORITHM]
            )
            return TokenPayload(**payload_dict)
        except (jwt.PyJWTError, KeyError):
            return None
