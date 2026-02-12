"""Сервис обеспечения безопасности и аутентификации."""

import logging
from dataclasses import asdict
from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash
from pwdlib.exceptions import PwdlibError
from pwdlib.hashers.argon2 import Argon2Hasher

from app.domain.entities.token import TokenPayloadEntity
from app.domain.interfaces.security import ISecurityService

logger = logging.getLogger(__name__)


class SecurityService(ISecurityService):
    def __init__(self, secret_key: str, algorithm: str, expire_minutes: int):
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._expire_minutes = expire_minutes
        self._password_hash = PasswordHash((Argon2Hasher(),))

    def hash_password(self, password: str) -> str:
        return self._password_hash.hash(password=password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        try:
            return self._password_hash.verify(plain_password, hashed_password)
        except PwdlibError as e:
            logger.error(f"Critical security error during password verification: {e}")
            return False

    def create_access_token(self, payload: TokenPayloadEntity) -> str:
        data_to_encode = asdict(payload)
        expire = datetime.now(UTC) + timedelta(minutes=self._expire_minutes)
        data_to_encode.update({"exp": int(expire.timestamp())})
        return jwt.encode(data_to_encode, self._secret_key, algorithm=self._algorithm)

    def decode_token(self, token: str) -> TokenPayloadEntity | None:
        try:
            payload_dict = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            return TokenPayloadEntity(
                sub=payload_dict["sub"],
                user_id=payload_dict["user_id"],
                exp=payload_dict.get("exp"),
            )
        except (jwt.PyJWTError, KeyError, TypeError):
            return None
