from abc import ABC, abstractmethod

from app.domain.entities.token import TokenPayloadEntity


class ISecurityService(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pass

    @abstractmethod
    def create_access_token(self, payload: TokenPayloadEntity) -> str:
        pass

    @abstractmethod
    def decode_token(self, token: str) -> TokenPayloadEntity | None:
        pass
