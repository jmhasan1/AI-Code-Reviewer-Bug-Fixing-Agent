from fastapi import FastAPI

from app.config.settings import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description=(
        "An agentic AI system for reviewing software repositories, "
        "identifying bugs, generating fixes, and validating changes."
    ),
    version=settings.app_version,
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Return application health status."""
    return {
        "status": "ok",
        "version": settings.app_version,
        "environment": settings.environment,
    }