from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import health
from app.core.config import settings
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(title=settings.app_name, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
