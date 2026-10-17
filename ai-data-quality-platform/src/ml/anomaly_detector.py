import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional

from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline


def load_model(path: str = 'models/isolation_forest.joblib'):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f'Model file not found: {path}')
    return joblib.load(p)


def preprocess_features(df: pd.DataFrame) -> pd.DataFrame:
    X = df.copy()
    feature_cols = []
    for c in ['amount']:
        if c in X.columns:
            feature_cols.append(c)
    for c in ['status', 'country']:
        if c in X.columns:
            dummies = pd.get_dummies(X[c], prefix=c, drop_first=False)
            X = pd.concat([X, dummies], axis=1)
            feature_cols.extend(dummies.columns.tolist())
    if not feature_cols:
        num_cols = X.select_dtypes(include=[np.number]).columns.tolist()
        feature_cols = list(num_cols)
    return X[feature_cols]


def detect_anomalies(df: pd.DataFrame, model) -> pd.DataFrame:
    X = df.copy()
    X_feat = preprocess_features(X)
    try:
        preds = model.predict(X_feat)
        scores = model.decision_function(X_feat)
    except Exception:
        num = X.select_dtypes(include=[np.number])
        if num.empty:
            preds = np.ones(len(X))
            scores = np.zeros(len(X))
        else:
            try:
                preds = model.predict(num)
                scores = model.decision_function(num)
            except Exception:
                preds = np.ones(len(X))
                scores = np.zeros(len(X))
    result = X.copy()
    result['is_anomaly'] = (preds == -1)
    result['anomaly_score'] = scores
    return result


def compare_with_rules(ml_anomalies: pd.DataFrame, rule_failures: Dict[str, Any]) -> Dict[str, Any]:
    total_anomalies = int(ml_anomalies['is_anomaly'].sum()) if 'is_anomaly' in ml_anomalies.columns else 0
    failed_row_ids = set()
    for _, info in rule_failures.items():
        for row in info.get('failed_rows', []):
            if isinstance(row, dict) and 'id' in row:
                try:
                    failed_row_ids.add(int(row['id']))
                except Exception:
                    pass
    ml_anomaly_ids = set()
    if 'is_anomaly' in ml_anomalies.columns:
        for _, r in ml_anomalies[ml_anomalies['is_anomaly']].iterrows():
            if 'id' in r:
                try:
                    ml_anomaly_ids.add(int(r['id']))
                except Exception:
                    pass
    not_covered = len(ml_anomaly_ids - failed_row_ids)
    pct_covered_by_rules = 0.0
    if total_anomalies > 0:
        pct_covered_by_rules = round((total_anomalies - not_covered) / total_anomalies * 100.0, 2)
    return {
        'total_detected': total_anomalies,
        'not_covered_by_rules': not_covered,
        'covered_by_rules_pct': pct_covered_by_rules,
        'ml_anomaly_ids': list(ml_anomaly_ids),
        'rule_failure_ids': list(failed_row_ids),
    }
