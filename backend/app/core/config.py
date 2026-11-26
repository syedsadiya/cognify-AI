from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")

    app_name: str = "CremaBench"
    tagline: str = "Intelligent Data. Smarter Performance."
    xai_api_key: str = ""
    xai_model: str = "grok-4.7"
    xai_base_url: str = "https://api.x.ai/v1"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    database_url: str = "sqlite:///./storage/cremabench.db"
    max_upload_mb: int = 200
    cors_origins: str = "http://localhost:5173"

    @property
    def upload_dir(self) -> Path:
        return BASE_DIR / "storage" / "uploads"

    @property
    def export_dir(self) -> Path:
        return BASE_DIR / "storage" / "exports"


settings = Settings()
