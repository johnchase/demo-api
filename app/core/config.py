"""Application settings."""
import secrets
from typing import List

from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    """Settings."""

    API_V1_STR: str = ""
    SECRET_KEY: str = secrets.token_urlsafe(32)
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    PROJECT_NAME: str = "Rupa Health API"

    MAILGUN_URL: str = "https://api.mailgun.net/v3/sandbox8b187dbcf9fd495fb74631a4c8bb1dee.mailgun.org/messages"
    MAILGUN_API_KEY: str = ""

    SENDGRID_URL: str = "https://api.sendgrid.com/v3/mail/send"
    SENDGRID_API_KEY: str = ""

    SEND_WITH_MAILGUN: bool = True

    class Config:
        """Settings configurations."""

        case_sensitive = True


settings = Settings()  # type: ignore
