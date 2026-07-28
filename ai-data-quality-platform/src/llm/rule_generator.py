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
