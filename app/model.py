import json
from pathlib import Path
from typing import Tuple

import joblib

MODEL_PATH = Path("artifacts/model.joblib")

def load_model(path: Path = MODEL_PATH):
    return joblib.load(path)

def predict_one(model, features) -> Tuple[int, float]:
    proba = model.predict_proba([features])[0]
    label = int(model.classes_[proba.argmax()])
    return label, float(proba.max())

def load_metrics(path: Path = Path("artifacts/metrics.json")) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))