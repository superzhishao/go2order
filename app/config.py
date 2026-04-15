from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Go2Run Order System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_PREFIX: str = "/api"

    # Database
    DATABASE_URL: str = "mysql+aiomysql://root:root@localhost:3306/go2run_drink?charset=utf8mb4"
    DATABASE_ECHO: bool = False

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT
    SECRET_KEY: str = "go2run-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # WeChat Mini App
    WX_MINI_APP_ID: Optional[str] = None
    WX_MINI_APP_SECRET: Optional[str] = None

    # WeChat Official Account
    WX_MP_APP_ID: Optional[str] = None
    WX_MP_APP_SECRET: Optional[str] = None

    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB

    # SMS
    SMS_ENABLED: bool = False

    model_config = {"env_file": ".env", "case_sensitive": True}


settings = Settings()
