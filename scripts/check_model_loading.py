import json
from pathlib import Path

from app.model import load_model, predict_one

model = load_model(Path("artifacts/model.joblib"))
label, probability = predict_one(model, [0.0] * 5)
assert label in (0, 1)
assert 0.0 <= probability <= 1.0
print(json.dumps({"MODEL_LOADING": "PASS", "prediction": label}))
