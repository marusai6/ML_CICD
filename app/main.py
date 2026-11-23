import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.model import load_model, predict_one
from app.preprocess import preprocess_features

APP_VERSION = "1.0.0"

app = FastAPI(title="ML API")
model = load_model()
MODEL_VERSION = f"sha-{Path('artifacts/model.joblib').stat().st_mtime_ns}"

class PredictRequest(BaseModel):
    features: list[float]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ready")
def ready():
    return {"status": "ready" if model is not None else "not_ready"}

@app.get("/version")
def version():
    return {"app_version": APP_VERSION, "model_version": MODEL_VERSION}

@app.post("/predict")
def predict(req: PredictRequest):
    try:
        features = preprocess_features(req.features)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    label, proba = predict_one(model, features)
    return {
        "prediction": label,
        "probability": proba,
        "model_version": MODEL_VERSION,
        "request_id": str(uuid.uuid4()),
    }