from typing import Any

from fastapi import APIRouter

from app import schemas

router = APIRouter()


@router.post("/", response_model=schemas.Email)
def email(email: schemas.Email) -> Any:
    return email
