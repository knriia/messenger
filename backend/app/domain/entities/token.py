from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class TokenPayloadEntity:
    sub: str  # username
    user_id: int
    exp: int | None = None  # время истечения

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class TokenEntity:
    access_token: str
    token_type: str
