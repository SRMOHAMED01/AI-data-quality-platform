"""
report_generator.py
=====================

RÔLE DE CE FICHIER
-------------------
Assembler les résultats du rule_engine (règles SQL) ET de l'anomaly_detector
(ML) en UN SEUL rapport de qualité consolidé, exportable en JSON/HTML/CSV,
et consommé ensuite par le dashboard Streamlit et par notifier.py.

CE QU'IL FAUT IMPLÉMENTER
--------------------------
1. `build_report(rule_results: dict, ml_results: pd.DataFrame) -> dict` :
   construit un dict structuré, ex :
   {
     "run_timestamp": "...",
     "total_rows": 1000,
     "global_conformity_pct": 92.5,
     "rules": [
        {"column": "amount", "rule": "amount >= 0", "conformity_pct": 98.0, "severity": "high", "failed_count": 20},
        ...
     ],
     "ml_anomalies": {
        "total_detected": 15,
        "not_covered_by_rules": 6,
        "top_suspicious_rows": [...]
     }
   }

2. `export_json(report: dict, path: str)` : sauvegarde le rapport brut.

3. `export_html(report: dict, path: str)` : génère un rapport HTML lisible
   (utiliser Jinja2 avec un petit template, ou pandas `.to_html()` pour
   aller vite au début).

4. Bloc `if __name__ == "__main__":` qui enchaîne : charge les résultats
   des étapes précédentes → build_report → export_json + export_html.

POINTS D'ATTENTION
-------------------
- C'est CE dict `report` qui doit aussi être sauvegardé en base via
  `QualityRun` et `RuleResult` (src/db/models.py) pour garder un
  historique.
- Garde le format JSON stable dans le temps : le dashboard Streamlit va
  se baser dessus, donc évite de casser la structure entre deux runs.
"""

# TODO: import json, pandas as pd
# TODO: implémenter build_report, export_json, export_html
