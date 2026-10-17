import logging
import os
from pathlib import Path
from typing import Optional

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

logger = logging.getLogger(__name__)


def load_training_data(path: str = 'data/sample_transactions.csv') -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f'Training data not found: {path}')
    df = pd.read_csv(p)
    return df


def build_pipeline(numeric_cols=None, categorical_cols=None, contamination: float = 0.02) -> Pipeline:
    if numeric_cols is None:
        numeric_cols = ['amount']
    if categorical_cols is None:
        categorical_cols = ['status', 'country']
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols),
        ]
    )
    model = IsolationForest(contamination=contamination, random_state=42)
    return Pipeline([('preprocessor', preprocessor), ('model', model)])


def train_and_save(data_path: str = 'data/sample_transactions.csv', model_output_path: str = 'models/isolation_forest.joblib', contamination: float = 0.02) -> None:
    df = load_training_data(data_path)
    X = df.copy()
    numeric_cols = [c for c in ['amount'] if c in X.columns]
    categorical_cols = [c for c in ['status', 'country', 'email'] if c in X.columns]
    # keep minimal to avoid large feature space
    categorical_cols = [c for c in ['status', 'country'] if c in X.columns]
    pipeline = build_pipeline(numeric_cols=numeric_cols, categorical_cols=categorical_cols, contamination=contamination)
    X_feat = X
    try:
        pipeline.fit(X_feat)
    except Exception:
        X_feat = df[['amount']].copy() if 'amount' in df.columns else df.select_dtypes(include='number').copy()
        pipeline = build_pipeline(numeric_cols=list(X_feat.columns), categorical_cols=[], contamination=contamination)
        pipeline.fit(X_feat)
    out_path = Path(model_output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, out_path)
    logger.info('Model saved to %s', out_path)
