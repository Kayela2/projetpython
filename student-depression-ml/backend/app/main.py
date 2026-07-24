"""FastAPI application entrypoint."""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import settings
from .model_service import ModelNotLoadedError, get_model_service
from .routers import predict as predict_router
from .schemas import HealthResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        get_model_service()
        logger.info("Modèle chargé avec succès depuis %s", settings.model_path)
    except ModelNotLoadedError:
        logger.error("Échec du chargement du modèle au démarrage — /predict renverra 503.")
    yield


app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_origin_regex=settings.cors_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_router.router, prefix="/api")


@app.exception_handler(ModelNotLoadedError)
def handle_model_not_loaded(request: Request, exc: ModelNotLoadedError) -> JSONResponse:
    return JSONResponse(status_code=503, content={"detail": "Le modèle n'est pas disponible pour le moment."})


@app.exception_handler(RequestValidationError)
def handle_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"detail": "Données invalides.", "errors": exc.errors()},
    )


@app.get("/api/health", response_model=HealthResponse, tags=["health"])
def health() -> dict:
    try:
        service = get_model_service()
        return {"status": "ok", "model_loaded": True, "model_version": service.version}
    except ModelNotLoadedError:
        return {"status": "degraded", "model_loaded": False, "model_version": "n/a"}
