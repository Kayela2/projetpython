import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.model_service import DepressionModelService, get_model_service

VALID_PAYLOAD = {
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


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session")
def model_service() -> DepressionModelService:
    return get_model_service()


@pytest.fixture
def valid_payload() -> dict:
    return dict(VALID_PAYLOAD)
