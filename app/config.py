from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:secret@db:5432/audio_db"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:secret@db:5432/audio_db"
    YANDEX_OAUTH_CLIENT_ID: str
    YANDEX_OAUTH_CLIENT_SECRET: str
    YANDEX_OAUTH_REDIRECT_URI: str
    
    class Config:
        env_file = ".env"

settings = Settings()
