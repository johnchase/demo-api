"""Email endpoint test module."""
import json
from typing import Any

import pytest
import requests
from fastapi.testclient import TestClient

from app.core.config import settings


@pytest.fixture
def email_payload() -> dict[str, str]:
    """email_payload.

    Parameters
    ----------

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


def test_correct_payload(client: TestClient, email_payload: dict) -> None:
    """test_correct_payload.

    Test that a valid payload returns a 200 response

    Parameters
    ----------
    client : TestClient
        client

    Returns
    -------
    None

    """
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
