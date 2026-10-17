import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

logger = logging.getLogger(__name__)


def load_rules(path: str = 'rules/generated_rules.json') -> List[dict]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f'Rules file not found: {path}')
    with p.open('r', encoding='utf-8') as f:
        return json.load(f)


def load_data(path: str = 'data/sample_transactions.csv') -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f'Data file not found: {path}')
    df = pd.read_csv(p)
    return df


def apply_rule(df: pd.DataFrame, rule: dict) -> pd.Series:
    rule_sql = str(rule.get('rule_sql', '')).strip()
    if not rule_sql:
        raise ValueError('rule_sql is empty')
    try:
        mask = df.eval(rule_sql, engine='python')
    except Exception as e:
        raise ValueError(f'Failed to evaluate rule_sql: {e}')
    if not isinstance(mask, pd.Series):
        mask = pd.Series([bool(mask)] * len(df), index=df.index)
    return mask


def run_all_rules(df: pd.DataFrame, rules: List[dict]) -> Dict[str, Any]:
    results: Dict[str, Any] = {}
    for rule in rules:
        rule_key = rule.get('rule_sql') or rule.get('description') or 'rule'
        try:
            mask = apply_rule(df, rule)
            conforming = df[mask.astype(bool)]
            failing = df[~mask.astype(bool)]
            total = len(df)
            pass_count = len(conforming)
            fail_count = len(failing)
            conformity_pct = round((pass_count / total) * 100.0, 2) if total > 0 else 0.0
            failed_rows = failing.to_dict(orient='records')
            results[rule_key] = {
                'pass': pass_count,
                'fail': fail_count,
                'conformity_pct': conformity_pct,
                'failed_rows': failed_rows,
                'column': rule.get('column'),
                'severity': rule.get('severity'),
                'description': rule.get('description'),
            }
        except Exception as e:
            logger.warning('Skipping rule due to error: %s - %s', rule_key, e)
            results[rule_key] = {
                'pass': len(df),
                'fail': 0,
                'conformity_pct': 100.0,
                'failed_rows': [],
                'error': str(e),
            }
    return results
