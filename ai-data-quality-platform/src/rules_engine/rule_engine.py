"""
rule_engine.py
================

RÔLE DE CE FICHIER
-------------------
Appliquer les règles générées par le LLM (rules/generated_rules.json)
sur les vraies données (data/sample_transactions.csv ou la table en base),
et calculer le taux de conformité par règle.

CE QU'IL FAUT IMPLÉMENTER
--------------------------
1. `load_rules(path: str) -> list[dict]` : charge generated_rules.json

2. `load_data(path: str) -> pandas.DataFrame` : charge le dataset (CSV,
   ou requête SQLAlchemy si tu utilises PostgreSQL — voir src/db/)

3. `apply_rule(df: pd.DataFrame, rule: dict) -> pd.Series` :
   convertit le `rule_sql` (ex: "amount >= 0") en une expression
   évaluable sur le DataFrame.
   ⚠️ ATTENTION SÉCURITÉ : ne JAMAIS faire un `eval()` brut sur du texte
   généré par un LLM (risque d'injection de code). Utiliser plutôt :
     - `df.query(rule_sql)` (plus sûr, mais toujours valider le contenu
       de rule_sql avant, ex: whitelist de caractères autorisés), ou
     - un mini-parseur d'expressions simples avec une librairie comme
       `pandasql` ou en traduisant vers des opérations Pandas natives.

4. `run_all_rules(df: pd.DataFrame, rules: list[dict]) -> dict` :
   pour chaque règle, calcule :
     - nombre de lignes conformes / non conformes
     - % de conformité
     - liste des lignes en échec (pour debug / alerting)
   retourne un dict structuré, ex :
     {
       "amount >= 0": {"pass": 980, "fail": 20, "conformity_pct": 98.0, "failed_rows": [...]},
       ...
     }

5. Bloc `if __name__ == "__main__":` pour tester en standalone.

POINTS D'ATTENTION
-------------------
- Toujours logger les règles qui n'ont pas pu être appliquées (erreur de
  syntaxe dans le rule_sql généré par le LLM) plutôt que de planter tout
  le pipeline.
- Garder une trace des `failed_rows` (au moins les ids) pour que le
  rapport et le dashboard puissent les afficher.
"""

# TODO: import pandas as pd, json, logging
# TODO: implémenter load_rules, load_data, apply_rule, run_all_rules
