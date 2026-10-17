import pytest
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from src.ml.anomaly_detector import preprocess_features, detect_anomalies, compare_with_rules


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'amount': [10, 12, 15, 11, 1000],
        'status': ['completed', 'completed', 'pending', 'completed', 'failed'],
        'country': ['MA', 'FR', 'MA', 'ES', 'MA'],
    })


@pytest.fixture
def trained_model():
    df = pd.DataFrame({'amount': [10, 12, 15, 11, 13, 14, 16]})
    model = IsolationForest(random_state=42, contamination=0.01)
    model.fit(df)
    return model


def test_preprocess_features_returns_expected_columns(sample_df):
    X = preprocess_features(sample_df)
    assert not X.empty


def test_detect_anomalies_flags_obvious_outlier(sample_df, trained_model):
    res = detect_anomalies(sample_df, trained_model)
    assert 'is_anomaly' in res.columns
    assert 'anomaly_score' in res.columns


def test_anomaly_score_ordering(sample_df, trained_model):
    res = detect_anomalies(sample_df, trained_model)
    outlier = res[res['amount'] == 1000]
    assert not outlier.empty


def test_compare_with_rules_counts_correctly():
    ml_anomalies = pd.DataFrame({'id': [1, 2, 3], 'is_anomaly': [True, True, True]})
    rule_failures = {'r1': {'failed_rows': [{'id': 1}]}}
    cmp = compare_with_rules(ml_anomalies, rule_failures)
    assert 'total_detected' in cmp
    assert 'not_covered_by_rules' in cmp
    assert cmp['total_detected'] == 3
    assert cmp['not_covered_by_rules'] == 2
