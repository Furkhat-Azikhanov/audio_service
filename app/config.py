from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:secret@db:5432/audio_db"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:secret@db:5432/audio_db"
    YANDEX_OAUTH_CLIENT_ID: str
    YANDEX_OAUTH_CLIENT_SECRET: str
    YANDEX_OAUTH_REDIRECT_URI: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

    
    class Config:
        env_file = ".env"

settings = Settings()
