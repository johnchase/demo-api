import secrets
from typing import List

from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):

    API_V1_STR: str = ""
    SECRET_KEY: str = secrets.token_urlsafe(32)
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    PROJECT_NAME: str = "Rupa Health API"


settings = Settings.construct()
