from fastapi import APIRouter
from app.core.config import settings
from app.engines.registry import engine_status

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "tagline": settings.tagline,
        "engines": engine_status(),
    }
