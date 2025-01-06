import os
# from pydantic import BaseSettings
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Task Manager"
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017/task_manager")
    MONGO_USER: str = os.getenv("MONGO_USER", "admin")
    MONGO_PASS: str = os.getenv("MONGO_PASS", "secret")
    MYSQL_URI: str = os.getenv("MYSQL_URI", "mysql+pymysql://user:password@localhost/task_db")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecretkey")
    REDIS_URI: str = os.getenv("REDIS_URI", "redis://localhost:6379/0")
    MONGO_HOST: str = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT: int = os.getenv("MONGO_PORT", "27017")

settings = Settings()
