"""Loads the trained pipeline and turns raw requests into predictions + local explanations."""
import json
import logging
from pathlib import Path

import joblib
import pandas as pd

from .config import settings
from .schemas import FeatureContribution, PredictionRequest

logger = logging.getLogger(__name__)

FEATURE_LABELS = {
    "Age": "Âge",
    "CGPA": "Moyenne générale (CGPA)",
    "Sleep_Duration": "Durée de sommeil",
    "Study_Hours": "Heures d'étude",
    "Social_Media_Hours": "Heures sur les réseaux sociaux",
    "Physical_Activity": "Activité physique",
    "Stress_Level": "Niveau de stress",
    "Gender": "Genre",
    "Department": "Département",
}


class ModelNotLoadedError(RuntimeError):
    """Raised when the model/metadata artifacts can't be loaded from disk."""


class DepressionModelService:
    """Wraps the fitted sklearn Pipeline (preprocessing + Kernel SVM).

    Predictions come straight from the pipeline's `predict` / `predict_proba`.
    Per-prediction "explanations" use an occlusion (ablation) method: each
    feature is, in turn, replaced by its training-set baseline (mean for
    numeric, mode for categorical — see 04_Optimisation.ipynb) and the
    resulting shift in `decision_function` score is taken as that feature's
    marginal contribution. This is a lightweight, model-agnostic
    approximation (not a true Shapley value): SVC with an RBF kernel has no
    native feature_importances_, and a proper SHAP KernelExplainer would be
    too slow for a synchronous single-request API.
    """

    def __init__(self, model_path: Path, metadata_path: Path):
        try:
            self._pipeline = joblib.load(model_path)
            with open(metadata_path, encoding="utf-8") as f:
                self._metadata = json.load(f)
        except (FileNotFoundError, OSError) as exc:
            raise ModelNotLoadedError(f"Impossible de charger le modèle: {exc}") from exc

        self._numeric_features = self._metadata["features"]["numeric"]
        self._categorical_features = self._metadata["features"]["categorical"]
        self._feature_order = self._numeric_features + self._categorical_features
        self._baselines = self._metadata["feature_baselines"]
        params = self._metadata["best_params"]
        self._version = f"svm-rbf_C{params['C']}_gamma{params['gamma']}_cw-{params['class_weight']}"

    @property
    def metadata(self) -> dict:
        return self._metadata

    @property
    def version(self) -> str:
        return self._version

    def _to_frame(self, request: PredictionRequest) -> pd.DataFrame:
        row = {
            "Age": request.age,
            "Gender": request.gender,
            "Department": request.department,
            "CGPA": request.cgpa,
            "Sleep_Duration": request.sleep_duration,
            "Study_Hours": request.study_hours,
            "Social_Media_Hours": request.social_media_hours,
            "Physical_Activity": request.physical_activity,
            "Stress_Level": request.stress_level,
        }
        return pd.DataFrame([row])[self._feature_order]

    def _explain(self, X: pd.DataFrame, top_n: int = 5) -> list[FeatureContribution]:
        base_score = float(self._pipeline.decision_function(X)[0])
        contributions = []
        for col in self._feature_order:
            X_ablated = X.copy()
            X_ablated[col] = self._baselines[col]
            ablated_score = float(self._pipeline.decision_function(X_ablated)[0])
            delta = base_score - ablated_score
            if delta > 1e-6:
                direction = "increases_risk"
            elif delta < -1e-6:
                direction = "decreases_risk"
            else:
                direction = "neutral"
            contributions.append(
                FeatureContribution(
                    feature=col,
                    label=FEATURE_LABELS.get(col, col),
                    value=str(X[col].iloc[0]),
                    contribution=round(delta, 4),
                    direction=direction,
                )
            )
        contributions.sort(key=lambda c: abs(c.contribution), reverse=True)
        return contributions[:top_n]

    def predict(self, request: PredictionRequest) -> dict:
        X = self._to_frame(request)
        proba = self._pipeline.predict_proba(X)[0]
        # Deliberately not using self._pipeline.predict(X): SVC's .predict()
        # thresholds the raw decision_function at 0, while .predict_proba()
        # comes from a separately-fit Platt-scaling calibration — with
        # class_weight="balanced" the two can disagree near the boundary
        # (e.g. predict()=True while probability_depression < 0.5). Deriving
        # the boolean from the same probability we display keeps the API
        # response internally consistent.
        prediction = bool(proba[1] >= 0.5)

        return {
            "prediction": prediction,
            "prediction_label": (
                "Signes de dépression détectés" if prediction else "Pas de signes de dépression détectés"
            ),
            "probability_depression": round(float(proba[1]), 4),
            "probability_not_depression": round(float(proba[0]), 4),
            "confidence": round(float(max(proba)), 4),
            "top_factors": self._explain(X),
            "model_version": self._version,
        }


_service: DepressionModelService | None = None


def get_model_service() -> DepressionModelService:
    """FastAPI dependency: lazily loads and caches a single service instance."""
    global _service
    if _service is None:
        _service = DepressionModelService(settings.model_path, settings.metadata_path)
    return _service
