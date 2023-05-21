"""Email endpoint test module."""
import json
import os
from unittest.mock import patch

import pytest
import requests
from fastapi.testclient import TestClient

from app.core.config import settings


@pytest.fixture
def email_payload() -> dict[str, str]:
    """email_payload.

    Fixture for creating test email data

    Returns
    -------
    dict

    """
    return {
        "to": "fake@example.com",
        "to_name": "mr. fake",
        "from": "no-reply@fake.com",
        "from_name": "ms. fake",
        "subject": "a message from the fake family",
        "body": "<h1>your bill</h1><p>$10</p>",
    }


class _APIError(AssertionError):
    """Assertion of API error."""

    pass


def _assert_status(response: requests.Response):
    """_assert_status.

    Parameters
    ----------
    response : requests.Response
        response
    """
    try:
        response.raise_for_status()
    except Exception as e:
        raise _APIError(response.json()) from e


@patch.dict(os.environ, {"SEND_WITH_MAILGUN": "False"})
def test_correct_payload_sendgrid(client: TestClient, email_payload: dict) -> None:
    """test_correct_payload_sendgrid.

    Test that a valid payload returns a 200 response

    Parameters
    ----------
    client : TestClient
        client

    Returns
    -------
    None

    """
    settings.SEND_WITH_MAILGUN = False
    with patch("app.util.email.send_with_sendgrid") as mock_request:
        mock_request.return_value.ok = True
        response = client.post(f"{settings.API_V1_STR}/email/", json.dumps(email_payload))

    settings.SEND_WITH_MAILGUN = True
    _assert_status(response)


def test_correct_payload_mailgun(client: TestClient, email_payload: dict) -> None:
    """test_correct_payload_mailgun.

    Test that a valid payload returns a 200 response

    Parameters
    ----------
    client : TestClient
        client

    Returns
    -------
    None

    """
    with patch("app.util.email.send_with_mailgun") as mock_request:
        mock_request.return_value.ok = True
        response = client.post(f"{settings.API_V1_STR}/email/", json.dumps(email_payload))

    _assert_status(response)


def test_invalid_email_to(client: TestClient, email_payload: dict) -> None:
    """test_invalid_email_to.

    Test that an invalid email in the 'to' field returns 422

    Parameters
    ----------
    client : TestClient
        client

    Returns
    -------
    None

    """
    email_payload["to"] = "not an email"
    response = client.post(
        f"{settings.API_V1_STR}/email/",
        json.dumps(email_payload),
    )

    assert response.status_code == 422


def test_invalid_email_from(client: TestClient, email_payload: dict) -> None:
    """test_invalid_email_from.

    Test that an invalid email in the 'from' field returns 422

    Parameters
    ----------
    client : TestClient
        client

    Returns
    -------
    None

    """
    email_payload["from"] = "not an email"
    response = client.post(
        f"{settings.API_V1_STR}/email/",
        json.dumps(email_payload),
    )

    assert response.status_code == 422


def test_missing_fields(client: TestClient, email_payload: dict) -> None:
    """test_missing_fields.

    Test that a missing field returns 422

    Parameters
    ----------
    client : TestClient
        client

    Returns
    -------
    None

    """
    del email_payload["from_name"]
    email_payload["from"] = "not an email"
    response = client.post(
        f"{settings.API_V1_STR}/email/",
        json.dumps(email_payload),
    )

    assert response.status_code == 422


@patch("app.util.email.requests.post")
def test_mailgun_called_with(mock_request, client: TestClient, email_payload: dict):
    """test_mailgun_called_with.

    Check that parameters are passed correctly to the external API

    Parameters
    ----------
    mock_request :
        mock_request
    client : TestClient
        client
    email_payload : dict
        email_payload
    """
    client.post(
        f"{settings.API_V1_STR}/email/",
        json.dumps(email_payload),
    )
    auth = ("api", settings.MAILGUN_API_KEY)
    data = {
        "from": "ms. fake <no-reply@fake.com>",
        "to": "mr. fake <fake@example.com>",
        "subject": "a message from the fake family",
        "text": "# your bill\n\n$10\n\n",
    }
    mock_request.assert_called_with(settings.MAILGUN_URL, auth=auth, data=data)


@patch("app.util.email.requests.post")
def test_sendgrid_called_with(mock_request, client: TestClient, email_payload: dict):
    """test_sendgrid_called_with.

    Check that parameters are passed correctly to the external API

    Parameters
    ----------
    mock_request :
        mock_request
    client : TestClient
        client
    email_payload : dict
        email_payload
    """
    settings.SEND_WITH_MAILGUN = False
    client.post(
        f"{settings.API_V1_STR}/email/",
        json.dumps(email_payload),
    )
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {settings.SENDGRID_API_KEY}",
    }
    data = {
        "personalizations": [{"to": [{"email": "fake@example.com"}]}],
        "from": {"email": "no-reply@fake.com"},
        "subject": "a message from the fake family",
        "content": [{"type": "text/plain", "value": "# your bill\n\n$10\n\n"}],
    }

    settings.SEND_WITH_MAILGUN = True
    mock_request.assert_called_with(settings.SENDGRID_URL, headers=headers, json=data)
