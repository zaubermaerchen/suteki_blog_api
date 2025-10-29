from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    root_path: str = ""
    debug: bool = False
    database_url: str = ""
    cors_allow_origins: str = ""

    class Config:
        env_file = [".env", ".env.local"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
