"""
prompt_templates.py
=====================

RÔLE DE CE FICHIER
-------------------
Centraliser TOUS les prompts utilisés dans le projet, versionnés comme du
code (pas hardcodés dans rule_generator.py). Ça permet de :
- itérer sur un prompt sans toucher à la logique métier
- comparer facilement plusieurs versions d'un même prompt (v1, v2...)
- documenter pourquoi un prompt est formulé ainsi

CE QU'IL FAUT IMPLÉMENTER
--------------------------
1. `SYSTEM_PROMPT_RULE_GENERATION` (constante str) :
   décrit le rôle du LLM ("Tu es un expert en qualité de données...")
   et impose STRICTEMENT le format de sortie JSON, sans texte autour.

2. `build_rule_generation_prompt(schema: dict) -> str` :
   fonction qui prend le schema (chargé depuis table_schema.json) et
   construit le prompt final à envoyer au LLM, en injectant chaque
   colonne + sa description métier.

EXEMPLE DE STRUCTURE DE PROMPT À VISER
----------------------------------------
    System: "Tu es un expert en qualité de données. Tu réponds UNIQUEMENT
    en JSON valide, sans aucun texte avant ou après, sans balises markdown."

    User: "Voici le schéma d'une table :
    - amount (float): montant de la transaction, doit être positif
    - email (string): email du client, doit être un format valide
    ...

    Génère une liste de règles de validation au format JSON strict :
    [{\"column\": ..., \"rule_sql\": ..., \"description\": ..., \"severity\": \"high|medium|low\"}]"

POINTS D'ATTENTION
-------------------
- Toujours demander explicitement un format JSON strict + donner un
  exemple dans le prompt (few-shot) → réduit les erreurs de parsing.
- Ajouter un champ "severity" par règle : ça sert plus tard dans le
  dashboard pour prioriser les alertes.
"""

# TODO: définir SYSTEM_PROMPT_RULE_GENERATION
# TODO: implémenter build_rule_generation_prompt(schema)
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