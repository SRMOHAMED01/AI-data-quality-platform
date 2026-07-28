"""
app.py (Streamlit Dashboard)
==============================

RÔLE DE CE FICHIER
-------------------
Interface visuelle pour explorer le rapport de qualité de données de
façon interactive — c'est ce que tu montreras en démo/entretien.

CE QU'IL FAUT IMPLÉMENTER
--------------------------
1. **Page principale** (`st.title`, `st.sidebar`) :
   - Sélecteur du run à afficher (dernier run par défaut, ou historique
     via src/db si tu as branché PostgreSQL)

2. **Section "Vue d'ensemble"** :
   - `st.metric` pour afficher le % de conformité global, nombre total
     de lignes, nombre d'anomalies ML détectées
   - Un indicateur visuel coloré (vert/orange/rouge) selon le seuil de
     qualité

3. **Section "Règles générées par le LLM"** :
   - Tableau (`st.dataframe`) listant chaque règle, sa colonne, son %
     de conformité, sa sévérité
   - Barre de progression ou couleur conditionnelle par ligne
     (`st.dataframe` avec `.style.background_gradient` ou un tableau
     custom avec des emojis 🟢🟠🔴)

4. **Section "Anomalies détectées par le ML"** :
   - Graphique (`st.scatter_chart` ou Plotly) montrant les scores
     d'anomalie des transactions (mettre en évidence les points
     anormaux)
   - Tableau des transactions les plus suspectes (triées par
     anomaly_score)
   - Le chiffre clé à mettre en avant : "X anomalies détectées par le
     ML qui n'étaient PAS couvertes par les règles du LLM"

5. **Section "Prompts & règles brutes"** (bonus, pour la démo) :
   - Afficher le prompt envoyé au LLM et la réponse JSON brute reçue —
     ça rend la partie "IA" du projet tangible et impressionnante à
     montrer en entretien.

6. **Bouton "Relancer le pipeline"** (bonus) :
   - Un `st.button` qui déclenche manuellement l'exécution du pipeline
     complet (utile pour la démo sans dépendre d'Airflow qui tourne en
     arrière-plan).

COMMENT LANCER (à documenter dans le README aussi)
--------------------------------------------------------
    streamlit run dashboard/app.py

POINTS D'ATTENTION
-------------------
- Le dashboard doit lire les données depuis le rapport JSON généré par
  report_generator.py (ou depuis PostgreSQL si tu es allé jusque-là) —
  ne jamais recalculer la logique métier ici, uniquement afficher.
- Garder le fichier lisible : si ça grossit, découper en plusieurs
  fonctions `render_overview()`, `render_rules_section()`, etc.
"""

# TODO: import streamlit as st, pandas as pd, json
# TODO: charger le dernier rapport JSON (report/*.json)
# TODO: implémenter les sections décrites ci-dessus
