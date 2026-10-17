import json
import logging
import os
import re
from pathlib import Path
from typing import Any, List, Optional

from src.llm.llm_client import LLMClient, LLMRequestError
from src.llm.prompt_templates import (
    SYSTEM_PROMPT_RULE_GENERATION,
    build_rule_generation_prompt,
)

logger = logging.getLogger(__name__)


def load_schema(path: str = 'schema/table_schema.json') -> dict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f'Schema file not found: {path}')
    with p.open('r', encoding='utf-8') as f:
        return json.load(f)


def _strip_markdown_fences(text: str) -> str:
    if not text:
        return text
    t = text.strip()
    t = re.sub(r'^`(?:json)?\s*', '', t, flags=re.IGNORECASE)
    t = re.sub(r'\s*`$', '', t)
    return t.strip()


def validate_rules(rules: List[dict]) -> List[dict]:
    required = ['column', 'rule_sql', 'description', 'severity']
    valid: List[dict] = []
    for r in rules:
        if not isinstance(r, dict):
            logger.warning('Skipping non-dict rule: %s', r)
            continue
        missing = [k for k in required if k not in r]
        if missing:
            logger.warning('Skipping rule missing keys %s: %s', missing, r)
            continue
        valid.append({
            'column': str(r['column']),
            'rule_sql': str(r['rule_sql']),
            'description': str(r['description']),
            'severity': str(r['severity']),
        })
    return valid


def generate_rules(schema: dict, client: Optional[LLMClient] = None, max_retries: int = 3) -> List[dict]:
    if client is None:
        client = LLMClient()
    system_prompt = SYSTEM_PROMPT_RULE_GENERATION
    user_prompt = build_rule_generation_prompt(schema)
    last_error: Optional[Exception] = None
    for attempt in range(1, max_retries + 1):
        try:
            resp = client.complete(prompt=user_prompt, system_prompt=system_prompt)
            cleaned = _strip_markdown_fences(resp)
            data = json.loads(cleaned)
            if isinstance(data, dict) and 'rules' in data and isinstance(data['rules'], list):
                rules = data['rules']
            elif isinstance(data, list):
                rules = data
            else:
                raise ValueError('Unexpected JSON structure from LLM')
            validated = validate_rules(rules)
            if validated:
                return validated
            logger.warning('All rules rejected by validation on attempt %d', attempt)
        except json.JSONDecodeError as e:
            last_error = e
            logger.warning('JSON parse error on attempt %d: %s', attempt, e)
            if attempt < max_retries:
                user_prompt = user_prompt + '\n\nPREVIOUS RESPONSE WAS INVALID JSON. CORRECT IT AND RETURN ONLY VALID JSON. Error: ' + str(e)
        except Exception as e:
            last_error = e
            logger.warning('Error generating rules on attempt %d: %s', attempt, e)
    if last_error:
        raise last_error
    return []


def save_rules(rules, path: str = 'rules/generated_rules.json') -> None:
    import json
    from pathlib import Path
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('w', encoding='utf-8') as f:
        json.dump(rules, f, indent=2, ensure_ascii=False)
