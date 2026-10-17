import pytest
import pandas as pd
from src.rules_engine.rule_engine import apply_rule, run_all_rules


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'amount': [100, -5, 0, 50, 200, -1, 10, 20, 30, 40],
        'email': ['a@b.com', 'bad', 'c@d.com', 'e@f.com', 'g@h.com', 'i@j.com', 'k@l.com', 'm@n.com', 'o@p.com', 'q@r.com'],
    })


@pytest.fixture
def sample_rules():
    return [
        {'column': 'amount', 'rule_sql': 'amount >= 0', 'severity': 'high'},
        {'column': 'email', 'rule_sql': "email.str.contains('@')", 'severity': 'medium'},
    ]


def test_apply_rule_detects_violations(sample_df):
    rule = {'column': 'amount', 'rule_sql': 'amount >= 0', 'severity': 'high'}
    mask = apply_rule(sample_df, rule)
    assert mask.dtype == bool
    assert mask.iloc[1] == False
    assert mask.iloc[5] == False


def test_run_all_rules_returns_correct_structure(sample_df, sample_rules):
    result = run_all_rules(sample_df, sample_rules)
    assert 'amount >= 0' in result or 'email.str.contains(\'@\')' in result
    for k, v in result.items():
        assert 'pass' in v
        assert 'fail' in v
        assert 'conformity_pct' in v
        assert 'failed_rows' in v


def test_conformity_percentage_calculation(sample_df, sample_rules):
    result = run_all_rules(sample_df, [sample_rules[0]])
    key = 'amount >= 0'
    assert result[key]['conformity_pct'] == 80.0


def test_invalid_rule_sql_does_not_crash_pipeline(sample_df):
    rules = [{'column': 'amount', 'rule_sql': 'amount >> bad', 'severity': 'high'}]
    result = run_all_rules(sample_df, rules)
    assert isinstance(result, dict)
