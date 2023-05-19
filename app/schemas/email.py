"""Email schemas module."""
from pydantic import BaseModel, EmailStr


# Shared properties
class Email(BaseModel):
    """Email Base."""

    to: EmailStr
    to_name: str
    from_: EmailStr
    from_name: str
    subject: str
    body: str

    class Config:
        """Config."""

        # from is a reserced keyword in python and we can't use it directly
        fields = {"from_": "from"}
