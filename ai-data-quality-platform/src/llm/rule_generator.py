"""
rule_generator.py
===================

RÔLE DE CE FICHIER
-------------------
Orchestrer la génération des règles : charger le schéma, construire le
prompt (via prompt_templates.py), appeler le LLM (via llm_client.py),
parser la réponse JSON, valider sa structure, et sauvegarder le résultat
dans rules/generated_rules.json.

CE QU'IL FAUT IMPLÉMENTER
--------------------------
1. `load_schema(path: str) -> dict` : charge table_schema.json

2. `generate_rules(schema: dict) -> list[dict]` :
   - construit le prompt via `build_rule_generation_prompt`
   - appelle `LLMClient().complete(...)`
   - parse la réponse en JSON (`json.loads`)
   - IMPORTANT : le LLM peut parfois renvoyer du JSON mal formé ou
     entouré de ```json ... ``` → nettoyer la chaîne avant de parser
     (strip des balises markdown, retry si échec de parsing)

3. `validate_rules(rules: list[dict]) -> list[dict]` :
   vérifie que chaque règle a bien les clés attendues (column, rule_sql,
   description, severity), sinon la rejette et log un warning.

4. `save_rules(rules: list[dict], path: str)` :
   sauvegarde dans rules/generated_rules.json (créer le dossier `rules/`
   à la racine s'il n'existe pas).

5. Bloc `if __name__ == "__main__":` qui exécute le flux complet en
   standalone, pour pouvoir tester ce fichier isolément :
       python -m src.llm.rule_generator

GESTION DES ERREURS À PRÉVOIR
--------------------------------
- JSON invalide → retry (max 3 tentatives) avec un prompt de correction
  ("Le JSON précédent était invalide, corrige-le : ...")
- Timeout API → propager l'erreur avec un message clair

CE QUE ÇA DOIT PRODUIRE (exemple de sortie attendue dans generated_rules.json)
---------------------------------------------------------------------------------
[
  {
    "column": "amount",
    "rule_sql": "amount >= 0",
    "description": "Le montant doit être positif ou nul",
    "severity": "high"
  },
  {
    "column": "email",
    "rule_sql": "email LIKE '%_@_%._%'",
    "description": "L'email doit respecter un format basique valide",
    "severity": "medium"
  }
]
"""

# TODO: import json, os, logging
# TODO: from src.llm.llm_client import LLMClient
# TODO: from src.llm.prompt_templates import SYSTEM_PROMPT_RULE_GENERATION, build_rule_generation_prompt
# TODO: implémenter load_schema, generate_rules, validate_rules, save_rules
import json
from typing import Any


SYSTEM_PROMPT = """
You are an expert Data Quality Engineer.

Your task is to analyze a database table schema and generate
high-quality data validation rules.

You must:

1. Analyze every column.
2. Identify relevant data quality constraints.
3. Generate deterministic validation rules.
4. Avoid inventing business rules that are not supported by the schema.
5. Return ONLY valid JSON.
6. Do NOT return Markdown.
7. Do NOT wrap the response in ```json blocks.

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

The generated rules must be practical and executable against
a pandas DataFrame.

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
}
"""


def build_system_prompt() -> str:
    """
    Return the system prompt used for rule generation.
    """

    return SYSTEM_PROMPT.strip()


def build_user_prompt(schema: dict[str, Any]) -> str:
    """
    Build the user prompt from a table schema.

    Parameters
    ----------
    schema:
        Parsed JSON schema describing the table and its columns.

    Returns
    -------
    str
        Prompt containing the schema and generation instructions.
    """

    if not isinstance(schema, dict):
        raise TypeError("schema must be a dictionary")

    if "table_name" not in schema:
        raise ValueError("schema must contain 'table_name'")

    if "columns" not in schema:
        raise ValueError("schema must contain 'columns'")

    if not isinstance(schema["columns"], list):
        raise ValueError("'columns' must be a list")

    schema_json = json.dumps(
        schema,
        indent=2,
        ensure_ascii=False,
    )

    return f"""
Analyze the following database table schema.

Your objective is to generate data quality validation rules
for this table.

TABLE SCHEMA:

{schema_json}

GENERATION REQUIREMENTS:

1. Generate at least one useful validation rule for each relevant
   column.
2. Prefer rules directly supported by the column description.
3. Detect common quality problems such as:
   - null values
   - duplicates
   - invalid formats
   - invalid ranges
   - invalid categorical values
   - invalid dates
   - invalid country codes
4. The rule_sql field must contain a validation expression.
5. The description must explain what the rule validates.
6. Assign an appropriate severity.
7. Do not invent unsupported business constraints.
8. Return ONLY valid JSON.
9. Do not use Markdown.
10. Do not add explanations outside the JSON.

Return exactly this structure:

{{
  "rules": [
    {{
      "column": "column_name",
      "rule_sql": "validation expression",
      "description": "description",
      "severity": "medium"
    }}
  ]
}}
""".strip()