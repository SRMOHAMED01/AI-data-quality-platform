import json
import logging
import os
import re
from pathlib import Path
from typing import Any, List, Optional

from src.llm.llm_client import LLMClient, LLMRequestError

logger = logging.getLogger(__name__)

SYSTEM_PROMPT_RULE_GENERATION = '''You are an expert Data Quality Engineer.

Your task is to analyze a database table schema and generate
high-quality data validation rules.

You must:
1. Analyze every column.
2. Identify relevant data quality constraints.
3. Generate deterministic validation rules.
4. Avoid inventing business rules that are not supported by the schema.
5. Return ONLY valid JSON.
6. Do NOT return Markdown.
7. Do NOT wrap the response in `json blocks.

Each rule must contain exactly these fields:
- column
- rule_sql
- description
- severity

Allowed severity values:
- low
- medium
- high
- critical

The response MUST follow this structure:
{
  "rules": [
    {
      "column": "column_name",
      "rule_sql": "validation expression",
      "description": "human readable explanation",
      "severity": "medium"
    }
  ]
}'''


def build_rule_generation_prompt(schema: dict) -> str:
    if not isinstance(schema, dict):
        raise TypeError('schema must be a dictionary')
    for r in ['table_name', 'columns']:
        if r not in schema:
            raise ValueError('schema must contain ' + r)
    if not isinstance(schema['columns'], list):
        raise ValueError('columns must be a list')
    schema_json = json.dumps(schema, indent=2, ensure_ascii=False)
    return 'Analyze the following database table schema.\n\nTABLE SCHEMA:\n' + schema_json + '\n\nGenerate data quality validation rules. Return ONLY valid JSON in the required structure.'
