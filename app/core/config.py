from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASS: str
    POSTGRES_DB: str
    PATH_TO_STATIC: str
    DATABASE_HOST: str = 'db'

    @property
    def db_url(self) -> str:
        return (
            f'postgresql+asyncpg://'
            f'{self.POSTGRES_USER}:{self.POSTGRES_PASS}@{self.DATABASE_HOST}/{self.POSTGRES_DB}'
        )

    model_config = SettingsConfigDict(env_file=".env", extra='ignore')
