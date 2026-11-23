FEATURE_COUNT = 5

def preprocess_features(features):
    if len(features) != FEATURE_COUNT:
        raise ValueError(f"Expected exactly {FEATURE_COUNT} features, got {len(features)}")
    for value in features:
        if not isinstance(value, (int, float)) or value != value or value in (float("inf"), float("-inf")):
            raise ValueError("All feature values must be finite numbers")
    return [float(v) for v in features]
