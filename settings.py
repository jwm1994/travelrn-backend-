from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./dev.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    APP_ENV: str = "dev"

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()
