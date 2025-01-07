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


# if __name__ == "__main__":
#     print(f"App Name: {Settings.APP_NAME}")
#     print(f"Mongo URI: {Settings.MONGO_URI}")
#     print(f"Mongo User: {Settings.MONGO_USER}")
#     print(f"Mongo Password: {Settings.MONGO_PASS}")
#     print(f"MySQL URI: {Settings.MYSQL_URI}")
#     print(f"JWT Secret: {Settings.JWT_SECRET}")
#     print(f"Redis URI: {Settings.REDIS_URI}")
#     print(f"Mongo Host: {Settings.MONGO_HOST}")
#     print(f"Mongo Port: {Settings.MONGO_PORT}")
#     print(f"Number of Allowed Tasks: {Settings.NUM_ALLOWED_TASK}")
