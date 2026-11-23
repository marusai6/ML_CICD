import json
from pathlib import Path

def test_evaluation_metrics_meet_gate():
    metrics = json.loads(Path("artifacts/metrics.json").read_text(encoding="utf-8"))
    assert metrics["f1"] >= metrics["min_f1_required"]
    assert 0 <= metrics["precision"] <= 1
    assert 0 <= metrics["recall"] <= 1
    assert 0 <= metrics["roc_auc"] <= 1
    