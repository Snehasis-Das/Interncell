from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    DEBUG: bool = True
    REDIS_URL: str = "redis://localhost:6379/0"

    ALLOWED_ORIGINS: str = "http://localhost:5500"

    SENDGRID_API_KEY: str | None = None
    EMAIL_FROM: str | None = None
    GCP_BUCKET_NAME: str | None = None

    ENVIRONMENT: str = "development"

    MAX_UPLOAD_SIZE: int = 5242880
    MAX_UPLOADS_PER_USER: int = 10
    ALLOWED_UPLOAD_TYPES: str = "application/pdf"
    STORAGE_MODE: str = "local"

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


settings = Settings()
