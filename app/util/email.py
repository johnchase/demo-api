"""Email endpoint support functions."""
from typing import Any

import requests

from app import schemas
from app.core.config import settings


def send_email(email: schemas.Email) -> Any:
    """send_email.

    Parameters
    ----------
    email : schemas.Email
        email

    Returns
    -------
    Any

    """
    if settings.SEND_WITH_MAILGUN:
        return send_with_mailgun(email)
    else:
        return send_with_sendgrid(email)


def send_with_mailgun(email: schemas.Email):
    """send_with_mailgun.

    Parameters
    ----------
    email : schemas.Email
        email
    """
    auth = ("api", settings.MAILGUN_API_KEY)

    data = {
        "from": f"{email.from_name} <{email.from_}>",
        "to": f"{email.to_name} <{email.to}>",
        "subject": email.subject,
        "text": email.body,
    }
    return requests.post(settings.MAILGUN_URL, auth=auth, data=data)


def send_with_sendgrid(email: schemas.Email):
    """send_with_sendgrid.

    Parameters
    ----------
    email : schemas.Email
        email
    """
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {settings.SENDGRID_API_KEY}",
    }
    data = {
        "personalizations": [{"to": [{"email": email.to}]}],
        "from": {"email": email.from_},
        "subject": email.subject,
        "content": [{"type": "text/plain", "value": email.body}],
    }
    return requests.post(settings.SENDGRID_URL, headers=headers, json=data)
