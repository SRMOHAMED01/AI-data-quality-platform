"""
test_rule_engine.py
=====================

RÔLE DE CE FICHIER
-------------------
Tests unitaires (Pytest) pour src/rules_engine/rule_engine.py — vérifier
que l'application des règles sur un DataFrame de test donne les bons
résultats, SANS dépendre du LLM (pas d'appel API dans les tests).

CE QU'IL FAUT IMPLÉMENTER
--------------------------
1. Une fixture Pytest `sample_df` qui crée un petit DataFrame Pandas
   codé en dur (5-10 lignes), avec des cas volontairement valides ET
   invalides (montant négatif, email mal formé, etc.) — ça reproduit
   data/sample_transactions.csv mais en mémoire pour isoler le test.

2. Une fixture `sample_rules` avec 2-3 règles codées en dur (pas besoin
   du LLM ici), ex :
       [{"column": "amount", "rule_sql": "amount >= 0", "severity": "high"}]

3. `test_apply_rule_detects_violations()` :
   vérifie qu'une règle "amount >= 0" détecte bien la ligne avec un
   montant négatif dans `sample_df`.

4. `test_run_all_rules_returns_correct_structure()` :
   vérifie que `run_all_rules()` retourne bien un dict avec les clés
   attendues (pass, fail, conformity_pct, failed_rows) pour chaque règle.

5. `test_conformity_percentage_calculation()` :
   vérifie que le calcul du % de conformité est mathématiquement correct
   (ex: 8 lignes conformes sur 10 → 80.0%).

6. `test_invalid_rule_sql_does_not_crash_pipeline()` :
   vérifie qu'une règle mal formée (rule_sql invalide, comme le LLM
   pourrait en générer) est catchée proprement (log + skip) sans faire
   planter tout le pipeline.

COMMENT LANCER
----------------
    pytest tests/test_rule_engine.py -v

POINTS D'ATTENTION
-------------------
- Ne JAMAIS appeler l'API du LLM dans un test unitaire (coût, lenteur,
  non-déterminisme) — toujours travailler avec des règles/données codées
  en dur ou mockées.
"""

# TODO: import pytest, pandas as pd
# TODO: from src.rules_engine.rule_engine import apply_rule, run_all_rules
# TODO: implémenter les fixtures et tests décrits ci-dessus
