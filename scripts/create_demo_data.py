import argparse
from pathlib import Path

import pandas as pd
from sklearn.datasets import make_classification

FEATURES = [f"feature_{i}" for i in range(5)]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="data/demo.csv")
    args = parser.parse_args()
    X, y = make_classification(
        n_samples=1800, n_features=5, n_informative=4, n_redundant=1,
        n_classes=2, weights=[0.65, 0.35], class_sep=1.5, random_state=17,
    )
    frame = pd.DataFrame(X, columns=FEATURES)
    frame["target"] = y
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
    print(f"Wrote {len(frame)} rows to {path}")

if __name__ == "__main__":
    main()
