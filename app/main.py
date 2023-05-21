"""Application module."""
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware

from app import __version__
from app.api.api import api_router
from app.core.config import settings

description = """
Welcome to the Rupa Health technical evaluation! Thanks for taking the time to look over this API
"""

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=description,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version=__version__,
    contact={"name": "John Chase", "email": "john@jchase.org"},
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def custom_schema():
    """custom_schema."""
    # Use cached if available
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Rupa Health Technical Evaluation Email API",
        version=__version__,
        routes=app.routes,
    )
    openapi_schema["info"] = {
        "title": "Rupa Health Technical Evaluation Email API",
        "version": __version__,
        "description": "Use this API to send an email",
        "contact": {
            "name": "Get Help with this API",
            "email": "john@jchase.org",
        },
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_schema


@app.get("/")
async def root():
    """Health Check."""
    return {"message": "Hello Rupa!"}


app.include_router(api_router, prefix=settings.API_V1_STR)
