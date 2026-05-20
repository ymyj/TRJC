from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "TRJC Backend API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "root"
    MYSQL_DATABASE: str = "trjc_db"

    ENCRYPTION_KEY: str = "your-32-byte-encryption-key-here!!"

    JWT_SECRET_KEY: str = "trjc-secret-key-change-in-production-2024"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_SECONDS: int = 86400  # 24小时
    JWT_REFRESH_EXPIRE_SECONDS: int = 604800  # 7天

    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:3002", "http://localhost:5173", "http://localhost:5174"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
