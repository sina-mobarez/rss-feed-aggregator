import os
from dotenv import load_dotenv

from pathlib import Path
env_path = Path('core/.env')
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "FastBlog"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "fbdb")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    SEND_SMS_API_KEY: str = os.getenv("SEND_SMS_API_KEY")
    SEND_SMS_PATTERN_KEY: str = os.getenv("SEND_SMS_PATTERN_KEY")
    SEND_SMS_SENDER_NUMBER: str = os.getenv("SEND_SMS_SENDER_NUMBER")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")
    ALGORITHM = os.getenv("ALGORITHM")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")


settings = Settings()
