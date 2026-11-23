import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/demo.csv")
    parser.add_argument("--min-f1", type=float, default=0.75)
    args = parser.parse_args()

    df = pd.read_csv(args.data)
    X = df.drop(columns=["target"]).values
    y = df["target"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        "f1": float(f1_score(y_test, pred)),
        "precision": float(precision_score(y_test, pred)),
        "recall": float(recall_score(y_test, pred)),
        "roc_auc": float(roc_auc_score(y_test, proba)),
        "min_f1_required": args.min_f1,
    }
    print(json.dumps(metrics, indent=2))

    if metrics["f1"] < args.min_f1:
        raise SystemExit(f"F1 {metrics['f1']:.3f} < required {args.min_f1}")

    out = Path("artifacts")
    out.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, out / "model.joblib")
    (out / "metrics.json").write_text(json.dumps(metrics), encoding="utf-8")
    print("Saved artifacts to", out)

if __name__ == "__main__":
    main()
