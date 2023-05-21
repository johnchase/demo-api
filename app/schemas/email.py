import markdownify
from pydantic import BaseModel, EmailStr, validator


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

        # from is a reserved keyword in python and we can't use it directly in the schema
        fields = {"from_": "from"}

    @validator("body", pre=True)
    def parse_html(cls, value):
        """parse_html.

        Parameters
        ----------
        value :
            value
        """
        return markdownify.markdownify(value, heading_style="ATX")
