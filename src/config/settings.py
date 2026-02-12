from functools import lru_cache
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: int

    @computed_field
    @property
    def db_migration_url(self) -> str:
        # Migrations are generated locally from outside the container
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@localhost:{self.db_port}/{self.db_name}"


@lru_cache(maxsize=1)
def get_settings():
    return Settings()
