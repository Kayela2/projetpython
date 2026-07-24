import pytest

from app.model_service import DepressionModelService, ModelNotLoadedError
from app.schemas import PredictionRequest


def make_request(**overrides) -> PredictionRequest:
    defaults = dict(
        age=21,
        gender="Female",
        department="Science",
        cgpa=2.9,
        sleep_duration=6.5,
        study_hours=5.0,
        social_media_hours=4.0,
        physical_activity=60,
        stress_level=7,
    )
    defaults.update(overrides)
    return PredictionRequest(**defaults)


def test_service_loads_and_exposes_metadata(model_service: DepressionModelService):
    assert model_service.metadata["target"] == "Depression"
    assert "C" in model_service.metadata["best_params"]
    assert model_service.version.startswith("svm-rbf_")


def test_missing_artifacts_raise_model_not_loaded_error(tmp_path):
    with pytest.raises(ModelNotLoadedError):
        DepressionModelService(tmp_path / "missing.joblib", tmp_path / "missing.json")


def test_predict_returns_well_formed_response(model_service: DepressionModelService):
    result = model_service.predict(make_request())

    assert isinstance(result["prediction"], bool)
    assert 0.0 <= result["probability_depression"] <= 1.0
    assert 0.0 <= result["probability_not_depression"] <= 1.0
    assert result["probability_depression"] + result["probability_not_depression"] == pytest.approx(1.0, abs=1e-3)
    assert 1 <= len(result["top_factors"]) <= 5


def test_prediction_boolean_is_consistent_with_probability(model_service: DepressionModelService):
    """Regression test: prediction must always agree with the 0.5 threshold on
    probability_depression. SVC's .predict() and .predict_proba() can disagree
    near the decision boundary when class_weight="balanced" is used — the
    service must not surface that inconsistency to API consumers."""
    profiles = [
        make_request(stress_level=1, cgpa=3.8, sleep_duration=8),
        make_request(stress_level=9, cgpa=1.8, sleep_duration=3),
        make_request(stress_level=5, cgpa=2.5, sleep_duration=6),
    ]
    for profile in profiles:
        result = model_service.predict(profile)
        expected = result["probability_depression"] >= 0.5
        assert result["prediction"] == expected


def test_top_factors_sorted_by_absolute_contribution(model_service: DepressionModelService):
    result = model_service.predict(make_request())
    contributions = [abs(f.contribution) for f in result["top_factors"]]
    assert contributions == sorted(contributions, reverse=True)


def test_higher_stress_and_lower_cgpa_increase_risk(model_service: DepressionModelService):
    calm_profile = make_request(stress_level=1, cgpa=3.8, sleep_duration=8, study_hours=3)
    stressed_profile = make_request(stress_level=10, cgpa=1.7, sleep_duration=3, study_hours=10)

    calm_result = model_service.predict(calm_profile)
    stressed_result = model_service.predict(stressed_profile)

    assert stressed_result["probability_depression"] > calm_result["probability_depression"]
