"""Application settings, resolved once at import time."""
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Serenity Depression Risk API"
    app_version: str = "1.0.0"
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    # Vite auto-increments the port (5174, 5175, ...) whenever the default is
    # already taken, which broke CORS in dev when a stale dev server was
    # squatting on 5173. Match any localhost/127.0.0.1 port as a dev-only
    # fallback so this can't happen again.
    cors_origin_regex: str = r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$"
    # Set on Render to the deployed frontend's URL (e.g.
    # https://serenity-frontend.onrender.com) so production CORS works
    # without loosening the regex above beyond localhost.
    frontend_origin: str | None = None

    model_dir: Path = Path(__file__).resolve().parent.parent.parent / "models"
    model_path: Path = model_dir / "depression_svm_pipeline.joblib"
    metadata_path: Path = model_dir / "model_metadata.json"


settings = Settings()
if settings.frontend_origin:
    settings.cors_origins.append(settings.frontend_origin)
