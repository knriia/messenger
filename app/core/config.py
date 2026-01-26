from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    PATH_TO_STATIC: str
    DATABASE_HOST: str = 'db'
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def db_url(self) -> str:
        return (
            f'postgresql+asyncpg://'
            f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DATABASE_HOST}/{self.POSTGRES_DB}'
        )

    model_config = SettingsConfigDict(env_file=".env", extra='ignore')
