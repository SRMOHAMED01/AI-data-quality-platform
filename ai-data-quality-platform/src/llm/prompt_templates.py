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
