"""
train_model.py
================

RÔLE DE CE FICHIER
-------------------
Entraîner le modèle de détection d'anomalies (Isolation Forest) sur les
données historiques, puis le sauvegarder pour qu'anomaly_detector.py
puisse le charger et l'utiliser en inférence.

CE QU'IL FAUT IMPLÉMENTER
--------------------------
1. `load_training_data(path: str) -> pd.DataFrame` :
   charge le dataset d'entraînement (idéalement un historique plus
   large que le sample_transactions.csv utilisé pour les tests).

2. `build_pipeline() -> sklearn.pipeline.Pipeline` :
   crée un pipeline scikit-learn qui enchaîne :
   - preprocessing (StandardScaler sur les colonnes numériques,
     OneHotEncoder sur les catégorielles) via `ColumnTransformer`
   - le modèle `IsolationForest(contamination=0.02, random_state=42)`
     (le paramètre `contamination` = % attendu d'anomalies dans les
     données, à ajuster selon ton dataset)

3. `train_and_save(data_path: str, model_output_path: str)` :
   - charge les données
   - fit le pipeline
   - sauvegarde le pipeline complet (preprocessing + modèle) avec
     `joblib.dump(pipeline, model_output_path)`
   - affiche/loggue quelques métriques de sanité (ex: % d'anomalies
     détectées sur le jeu d'entraînement lui-même, distribution des
     scores)

4. Bloc `if __name__ == "__main__":` pour lancer l'entraînement en CLI :
       python -m src.ml.train_model

POINTS D'ATTENTION
-------------------
- IsolationForest est non-supervisé : pas besoin de labels "fraude/pas
  fraude", il apprend juste à isoler les points "différents du reste".
- Fixe toujours `random_state` pour la reproductibilité.
- Sauvegarde le modèle dans un dossier `models/` à la racine (à créer),
  ajouté au `.gitignore` si le fichier est trop gros pour Git.
"""

# TODO: import pandas as pd, joblib
# TODO: from sklearn.ensemble import IsolationForest
# TODO: from sklearn.pipeline import Pipeline
# TODO: from sklearn.compose import ColumnTransformer
# TODO: from sklearn.preprocessing import StandardScaler, OneHotEncoder
# TODO: implémenter load_training_data, build_pipeline, train_and_save
