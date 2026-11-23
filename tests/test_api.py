from fastapi.testclient import TestClient
from app.main import app

def test_health_and_version():
    with TestClient(app) as client:
        assert client.get("/health").status_code == 200
        body = client.get("/version").json()
        assert body["app_version"]
        assert body["model_version"]

def test_prediction_contract():
    with TestClient(app) as client:
        response = client.post("/predict", json={"features": [0, 0, 0, 0, 0]})
        assert response.status_code == 200
        body = response.json()
        assert body["prediction"] in (0, 1)
        assert 0 <= body["probability"] <= 1
        assert body["model_version"]
        assert body["request_id"]

def test_invalid_api_input_fails():
    with TestClient(app) as client:
        response = client.post("/predict", json={"features": [1, 2]})
        assert response.status_code == 422
