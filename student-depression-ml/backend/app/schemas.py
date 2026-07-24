"""Pydantic request/response models for the prediction API.

Numeric bounds mirror the observed ranges from the EDA (01_EDA.ipynb) so
obviously invalid input is rejected with a 422 before it ever reaches the
model.
"""
from typing import Literal

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    age: int = Field(..., ge=15, le=35, description="Âge de l'étudiant")
    gender: Literal["Female", "Male"]
    department: Literal["Science", "Engineering", "Medical", "Arts", "Business"]
    cgpa: float = Field(..., ge=0.0, le=4.0, description="Moyenne générale (0-4)")
    sleep_duration: float = Field(..., ge=0.0, le=16.0, description="Heures de sommeil / jour")
    study_hours: float = Field(..., ge=0.0, le=16.0, description="Heures d'étude / jour")
    social_media_hours: float = Field(..., ge=0.0, le=16.0, description="Heures sur les réseaux sociaux / jour")
    physical_activity: float = Field(..., ge=0.0, le=300.0, description="Activité physique (min/jour)")
    stress_level: int = Field(..., ge=1, le=10, description="Niveau de stress ressenti (1-10)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "age": 21,
                "gender": "Female",
                "department": "Science",
                "cgpa": 2.9,
                "sleep_duration": 6.5,
                "study_hours": 5.0,
                "social_media_hours": 4.0,
                "physical_activity": 60,
                "stress_level": 7,
            }
        }
    }


class FeatureContribution(BaseModel):
    feature: str
    label: str
    value: str
    contribution: float
    direction: Literal["increases_risk", "decreases_risk", "neutral"]


class PredictionResponse(BaseModel):
    prediction: bool
    prediction_label: str
    probability_depression: float
    probability_not_depression: float
    confidence: float
    top_factors: list[FeatureContribution]
    model_version: str


class ModelInfoResponse(BaseModel):
    target: str
    algorithm: str
    best_params: dict
    cv_f1_score: float
    test_metrics: dict
    test_roc_auc: float
    sample_size: int
    train_size: int
    test_size: int


class HealthResponse(BaseModel):
    status: Literal["ok", "degraded"]
    model_loaded: bool
    model_version: str
