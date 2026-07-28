"""
data_quality_dag.py
=====================

RÔLE DE CE FICHIER
-------------------
Définir le DAG Airflow qui orchestre le pipeline complet, du début à la
fin, de façon planifiée (ex: tous les jours à 6h du matin).

ÉTAPES DU DAG À IMPLÉMENTER (en tâches Airflow, dans cet ordre)
--------------------------------------------------------------------
1. `generate_rules_task`     → appelle src/llm/rule_generator.py
   (peut être sauté si les règles existent déjà et qu'on ne veut pas
   regénérer à chaque run — ajouter un paramètre `force_regenerate`)

2. `apply_rules_task`        → appelle src/rules_engine/rule_engine.py

3. `detect_anomalies_task`   → appelle src/ml/anomaly_detector.py
   (utilise le modèle déjà entraîné ; l'entraînement lui-même,
   train_model.py, tourne dans un DAG séparé, moins fréquent, ex:
   hebdomadaire)

4. `build_report_task`       → appelle src/report/report_generator.py

5. `save_to_db_task`         → sauvegarde le run + résultats en base
   (src/db/models.py — QualityRun, RuleResult)

6. `alert_if_needed_task`    → appelle src/alerting/notifier.py,
   conditionné par `should_alert(report)`

DÉPENDANCES ENTRE TÂCHES (ordre d'exécution)
------------------------------------------------
    generate_rules_task >> apply_rules_task >> detect_anomalies_task
        >> build_report_task >> save_to_db_task >> alert_if_needed_task

CE QU'IL FAUT IMPLÉMENTER TECHNIQUEMENT
--------------------------------------------
- Utiliser `PythonOperator` pour chaque tâche (le plus simple pour
  démarrer), chaque tâche appelle une fonction Python qui elle-même
  importe et exécute le module correspondant.
- Définir le DAG avec :
    - `schedule_interval="@daily"`
    - `retries=2`, `retry_delay=timedelta(minutes=5)`
    - `catchup=False`
- Ajouter des `on_failure_callback` pour logger/alerter en cas d'échec
  d'une tâche elle-même (différent d'une alerte "qualité de données" —
  ici c'est une alerte "le pipeline a planté").

POINTS D'ATTENTION
-------------------
- Chaque tâche doit être idempotente (ré-exécutable sans effet de bord
  si elle est relancée après un échec).
- Ne pas mettre de logique métier directement dans le DAG : le DAG ne
  fait qu'ORCHESTRER, toute la logique reste dans src/.
"""

# TODO: from airflow import DAG
# TODO: from airflow.operators.python import PythonOperator
# TODO: from datetime import datetime, timedelta
# TODO: définir default_args, le DAG, les PythonOperator, et les dépendances >>
