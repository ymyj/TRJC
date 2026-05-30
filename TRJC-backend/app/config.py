from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_NAME: str = "TRJC Backend API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT: int = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "root")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE", "trjc_db")

    ENCRYPTION_KEY: str = os.getenv("ENCRYPTION_KEY", "your-32-byte-encryption-key-here!!")

    JWT_SECRET_KEY: str = "trjc-secret-key-change-in-production-2024"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_SECONDS: int = 86400  # 24小时
    JWT_REFRESH_EXPIRE_SECONDS: int = 604800  # 7天

    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:3002", "http://localhost:5173", "http://localhost:5174"]


settings = Settings()
