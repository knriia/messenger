import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from datetime import datetime, timedelta, timezone

from app.core.config import Settings


class SecurityService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.password_hash = PasswordHash((Argon2Hasher(),))

    def hash_password(self, password: str) -> str:
        return self.password_hash.hash(password=password)


    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.password_hash.verify(plain_password, hashed_password)


    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.settings.SECRET_KEY, algorithm=self.settings.ALGORITHM)

    def decode_token(self, token: str) -> dict | None:
        try:
            return jwt.decode(
                token,
                self.settings.SECRET_KEY,
                algorithms=[self.settings.ALGORITHM]
            )
        except (jwt.PyJWTError, KeyError):
            return None
