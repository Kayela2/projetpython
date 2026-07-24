"""Prediction and model-info endpoints."""
import logging

from fastapi import APIRouter, Depends, HTTPException

from ..model_service import DepressionModelService, get_model_service
from ..schemas import ModelInfoResponse, PredictionRequest, PredictionResponse

logger = logging.getLogger(__name__)
router = APIRouter(tags=["prediction"])


@router.post("/predict", response_model=PredictionResponse)
def predict(
    payload: PredictionRequest,
    service: DepressionModelService = Depends(get_model_service),
) -> dict:
    try:
        return service.predict(payload)
    except Exception as exc:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail="Erreur interne lors de la prédiction.") from exc


@router.get("/model/info", response_model=ModelInfoResponse)
def model_info(service: DepressionModelService = Depends(get_model_service)) -> dict:
    meta = service.metadata
    return {
        "target": meta["target"],
        "algorithm": "Kernel SVM (RBF)",
        "best_params": meta["best_params"],
        "cv_f1_score": meta["cv_f1_score"],
        "test_metrics": meta["test_metrics"],
        "test_roc_auc": meta["test_roc_auc"],
        "sample_size": meta["sample_size"],
        "train_size": meta["train_size"],
        "test_size": meta["test_size"],
    }
