import pytest
from unittest.mock import patch
from src.llm.rule_generator import generate_rules, validate_rules


def test_parses_clean_json_response():
    schema = {'table_name': 't', 'columns': [{'column': 'amount', 'type': 'float'}]}
    with patch('src.llm.rule_generator.LLMClient') as MockClient:
        instance = MockClient.return_value
        instance.complete.return_value = '[{"column": "amount", "rule_sql": "amount >= 0", "description": "d", "severity": "high"}]'
        rules = generate_rules(schema, client=instance)
        assert len(rules) > 0


def test_strips_markdown_code_fences():
    schema = {'table_name': 't', 'columns': [{'column': 'amount', 'type': 'float'}]}
    with patch('src.llm.rule_generator.LLMClient') as MockClient:
        instance = MockClient.return_value
        instance.complete.return_value = '`json\n[{"column": "amount", "rule_sql": "amount >= 0", "description": "d", "severity": "high"}]\n`'
        rules = generate_rules(schema, client=instance)
        assert len(rules) > 0


def test_validate_rules_rejects_missing_keys():
    bad = [{'column': 'amount'}]
    valid = validate_rules(bad)
    assert valid == []


def test_validate_rules_accepts_well_formed_rules():
    good = [{'column': 'amount', 'rule_sql': 'amount >= 0', 'description': 'd', 'severity': 'high'}]
    valid = validate_rules(good)
    assert valid == good


def test_generate_rules_retries_on_invalid_json():
    schema = {'table_name': 't', 'columns': [{'column': 'amount', 'type': 'float'}]}
    with patch('src.llm.rule_generator.LLMClient') as MockClient:
        instance = MockClient.return_value
        instance.complete.side_effect = ['{invalid', '[{"column": "amount", "rule_sql": "amount >= 0", "description": "d", "severity": "high"}]']
        rules = generate_rules(schema, client=instance)
        assert len(rules) > 0
        assert instance.complete.call_count == 2
