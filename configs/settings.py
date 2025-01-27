import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), verbose=True)

IS_DEBUG = os.getenv("IS_DEBUG", "0")
APP_PORT = os.getenv("APP_PORT", "8000")
APP_NAME = os.getenv("APP_NAME", "Placeholder")
APP_DB_CONNECTION_STRING = os.getenv("APP_DB_CONNECTION_STRING", "")
API_PREFIX = os.getenv("API_PREFIX", "/v1")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "Placeholder")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRED_IN_SECOND = os.getenv("JWT_EXPIRED_IN_SECOND", 3600)

ROLE_HIERARCHY = ["user", "admin", "super admin"]
LOG_MAX_LENGTH = 2500