from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:secret@db:5432/audio_db"

    class Config:
        env_file = ".env"

settings = Settings()
