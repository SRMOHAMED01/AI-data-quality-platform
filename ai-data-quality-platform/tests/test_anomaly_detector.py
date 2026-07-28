"""
test_anomaly_detector.py
===========================

RÔLE DE CE FICHIER
-------------------
Tests unitaires pour src/ml/anomaly_detector.py — vérifier que le
préprocessing et la détection d'anomalies fonctionnent correctement sur
des données de test connues.

CE QU'IL FAUT IMPLÉMENTER
--------------------------
1. Une fixture `sample_df` avec des données synthétiques où on connaît
   à l'avance quels points sont "normaux" et lesquels sont des
   "anomalies évidentes" (ex: un montant 100x plus élevé que les autres).

2. Une fixture `trained_model` : entraîne un petit `IsolationForest` à la
   volée sur des données synthétiques (pas besoin de charger un vrai
   modèle depuis disque dans les tests).

3. `test_preprocess_features_returns_expected_columns()` :
   vérifie que `preprocess_features()` retourne bien les colonnes
   attendues après encodage/normalisation.

4. `test_detect_anomalies_flags_obvious_outlier()` :
   vérifie que le point volontairement aberrant (montant énorme) est
   bien flaggé `is_anomaly = True`.

5. `test_anomaly_score_ordering()` :
   vérifie que le point aberrant a bien le score d'anomalie le plus bas
   (donc le plus suspect) parmi tous les points.

6. `test_compare_with_rules_counts_correctly()` :
   teste `compare_with_rules()` avec un jeu d'anomalies ML connu et un
   jeu de résultats de règles connu, vérifie que le calcul du nombre
   d'anomalies "non couvertes par les règles" est correct.

COMMENT LANCER
----------------
    pytest tests/test_anomaly_detector.py -v

POINTS D'ATTENTION
-------------------
- Fixe toujours `random_state` dans les tests pour avoir des résultats
  reproductibles (sinon le test peut devenir flaky).
"""

# TODO: import pytest, pandas as pd, numpy as np
# TODO: from sklearn.ensemble import IsolationForest
# TODO: from src.ml.anomaly_detector import preprocess_features, detect_anomalies, compare_with_rules
# TODO: implémenter les fixtures et tests décrits ci-dessus
