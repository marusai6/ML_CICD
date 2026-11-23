import argparse
import sys

import pandas as pd

FEATURES = [f"feature_{i}" for i in range(5)]
REQUIRED = FEATURES + ["target"]

def validate(path: str) -> None:
    frame = pd.read_csv(path)
    missing = sorted(set(REQUIRED) - set(frame.columns))
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    if len(frame) < 500:
        raise ValueError(f"Dataset too small: {len(frame)} rows; require >= 500")
    if frame[REQUIRED].isna().any().any():
        raise ValueError("Null values found in required columns")
    if not all(pd.api.types.is_numeric_dtype(frame[c]) for c in FEATURES):
        raise ValueError("All features must be numeric")
    if not set(frame["target"].unique()).issubset({0, 1}):
        raise ValueError("target must contain only 0 and 1")
    if frame["target"].nunique() != 2:
        raise ValueError("Both target classes must be present")
    print(f"DATA_VALIDATION=PASS rows={len(frame)} features={len(FEATURES)}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default="data/demo.csv")
    args = parser.parse_args()
    try:
        validate(args.path)
    except Exception as exc:
        print(f"DATA_VALIDATION=FAIL reason={exc}", file=sys.stderr)
        raise SystemExit(1) from exc

if __name__ == "__main__":
    main()