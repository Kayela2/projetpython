from fastapi.testclient import TestClient


def test_health_reports_model_loaded(client: TestClient):
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["model_loaded"] is True


def test_model_info_returns_metrics(client: TestClient):
    response = client.get("/api/model/info")
    assert response.status_code == 200
    body = response.json()
    assert body["target"] == "Depression"
    assert body["algorithm"] == "Kernel SVM (RBF)"
    assert "f1" in body["test_metrics"]


def test_predict_valid_payload_returns_200(client: TestClient, valid_payload: dict):
    response = client.post("/api/predict", json=valid_payload)
    assert response.status_code == 200
    body = response.json()
    assert set(body.keys()) == {
        "prediction",
        "prediction_label",
        "probability_depression",
        "probability_not_depression",
        "confidence",
        "top_factors",
        "model_version",
    }


def test_predict_rejects_out_of_range_stress_level(client: TestClient, valid_payload: dict):
    valid_payload["stress_level"] = 99
    response = client.post("/api/predict", json=valid_payload)
    assert response.status_code == 422


def test_predict_rejects_unknown_department(client: TestClient, valid_payload: dict):
    valid_payload["department"] = "Philosophy"
    response = client.post("/api/predict", json=valid_payload)
    assert response.status_code == 422


def test_predict_rejects_missing_field(client: TestClient, valid_payload: dict):
    del valid_payload["cgpa"]
    response = client.post("/api/predict", json=valid_payload)
    assert response.status_code == 422


def test_predict_rejects_negative_sleep(client: TestClient, valid_payload: dict):
    valid_payload["sleep_duration"] = -1
    response = client.post("/api/predict", json=valid_payload)
    assert response.status_code == 422
