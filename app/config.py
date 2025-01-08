import os
from dotenv import load_dotenv
from typing import ClassVar

load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME")
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_USER = os.getenv("MONGO_USER")
    MONGO_PASS = os.getenv("MONGO_PASS")
    MYSQL_URI = os.getenv("MYSQL_URI")
    JWT_SECRET = os.getenv("JWT_SECRET")
    REDIS_URI = os.getenv("REDIS_URI")
    MONGO_HOST = os.getenv("MONGO_HOST")
    MONGO_PORT = int(os.getenv("MONGO_PORT"))
    NUM_ALLOWED_TASK: ClassVar[int] = int(os.getenv("NUM_ALLOWED_TASK"))

    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
