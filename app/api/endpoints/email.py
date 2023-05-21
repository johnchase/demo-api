from typing import Any

from fastapi import APIRouter

from app import schemas, util

router = APIRouter()


@router.post(
    "/",
    response_model=dict[str, str],
    summary="Send an email",
    # description="Send and email through a third party email service. ",
)
def email(email: schemas.Email) -> Any:
    """
    **NOTE:** This API will return a 200 as long as a valid request is submitted to the third party email service.
    This means that a 200 doesn't guarantee a successful email was sent. Consult the response body for more
    information.
    All parameters listed are required
    - **to**: Must be a valid email address, the address where you would like to send an email
    - **to_name**: The name of the person you would like to sent an email to
    - **from**: Must be a valid email address, the address you would like
    to send the email from. This must be configured ahead of time with the
    third party providers
    - **from_name**: The name of the person sending the email
    - **Subject**: The subject line of the email
    - **Body**: The body of the email

    Parameters
    ----------
    email : schemas.Email
        email

    Returns
    -------
    Anyj
    """
    response = util.send_email(email)

    # This will return 200 regardless of the email server response,
    # this may or may not be the correct way to handle it
    # depending on what the application requirements are
    return {"External Server Response": response.status_code}
