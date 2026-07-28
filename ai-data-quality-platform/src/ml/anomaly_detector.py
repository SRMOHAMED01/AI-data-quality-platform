"""
anomaly_detector.py
=====================

RÔLE DE CE FICHIER
-------------------
Détecter les anomalies "subtiles" que les règles SQL générées par le LLM
ne peuvent PAS capter — par exemple une combinaison inhabituelle de
montant + heure + pays, même si chaque valeur individuelle est "valide".
C'est ici qu'on utilise du Machine Learning non-supervisé.

CE QU'IL FAUT IMPLÉMENTER
--------------------------
1. `load_model(path: str)` : charge un modèle déjà entraîné (pickle/joblib)

2. `preprocess_features(df: pd.DataFrame) -> pd.DataFrame` :
   - sélectionner les colonnes numériques pertinentes (amount, heure de
     la transaction extraite de transaction_date, etc.)
   - encoder les colonnes catégorielles (country, status) en one-hot ou
     label encoding
   - normaliser les features numériques (StandardScaler)

3. `detect_anomalies(df: pd.DataFrame, model) -> pd.DataFrame` :
   - utilise `model.predict(X)` (Isolation Forest retourne -1 pour
     anomalie, 1 pour normal)
   - ajoute une colonne `is_anomaly` (bool) et `anomaly_score`
     (`model.decision_function(X)`, plus le score est bas plus c'est
     suspect) au DataFrame original
   - retourne le DataFrame enrichi

4. `compare_with_rules(ml_anomalies: pd.DataFrame, rule_failures: dict) -> dict` :
   fonction "bonus" qui calcule combien d'anomalies détectées par le ML
   n'étaient PAS détectées par les règles SQL du LLM. C'est LA métrique à
   mettre en avant dans le README / en entretien :
   "Le modèle ML a détecté X% d'anomalies non couvertes par les règles
   générées par le LLM"

MODÈLE À UTILISER (pour commencer)
--------------------------------------
`sklearn.ensemble.IsolationForest` — simple, rapide, pas besoin de
labels (non supervisé), bien adapté à la détection de fraude/anomalies.

Version "harder" (bonus, si tu veux aller plus loin) :
un autoencoder simple avec Keras/PyTorch : on entraîne le modèle à
reconstruire les transactions normales, et une erreur de reconstruction
élevée = anomalie potentielle.

POINTS D'ATTENTION
-------------------
- Le modèle doit être entraîné UNIQUEMENT sur des données considérées
  comme "normales" (train_model.py s'en charge).
- Toujours sauvegarder le scaler avec le modèle (les deux doivent être
  cohérents au moment de la prédiction).
"""

# TODO: import pandas as pd, joblib, sklearn.preprocessing
# TODO: implémenter load_model, preprocess_features, detect_anomalies, compare_with_rules
