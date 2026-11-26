from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import health, datasets, benchmarks, dashboard, settings as settings_api, assistant
from app.core.config import settings
from app.core.logging import setup_logging
from app.db.database import init_db

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.app_name, version="0.2.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_methods=["*"],
    allow_headers=["*"],
)

for module in (health, datasets, benchmarks, dashboard, settings_api, assistant):
    app.include_router(module.router, prefix="/api")
