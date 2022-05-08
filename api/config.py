# -*- coding: utf-8 -*-
from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    debug: bool = False
    database_url: str
    cors_allow_origins: str = ""

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()