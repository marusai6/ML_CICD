import pytest
from app.preprocess import preprocess_features

def test_valid_features_keep_order():
    assert preprocess_features([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

@pytest.mark.parametrize("features", [[1, 2], [1, 2, 3, 4, 5, 6]])
def test_wrong_feature_count_fails(features):
    with pytest.raises(ValueError, match="exactly 5"):
        preprocess_features(features)

@pytest.mark.parametrize("bad_value", [float("nan"), float("inf"), -float("inf")])
def test_non_finite_features_fail(bad_value):
    with pytest.raises(ValueError, match="finite"):
        preprocess_features([1, 2, 3, 4, bad_value])
        