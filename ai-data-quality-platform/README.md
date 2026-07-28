# AI-Augmented Data Quality & Anomaly Detection Platform

> Plateforme qui combine **génération de règles de qualité par LLM** (Azure
> OpenAI) et **détection d'anomalies par Machine Learning** (Isolation
> Forest), orchestrée via Airflow, dockerisée, testée et intégrée en CI.

## CE QU'IL RESTE À FAIRE DANS CE README
- [ ] Remplacer ce paragraphe par un vrai résumé (2-3 phrases) du projet
- [ ] Ajouter un schéma d'architecture (dessine-le avec draw.io / excalidraw,
      exporte en PNG, mets-le dans `docs/architecture.png`, référence-le ici)
- [ ] Ajouter un GIF ou des screenshots du dashboard une fois qu'il tourne
- [ ] Ajouter le badge CI une fois que `.github/workflows/ci.yml` fonctionne :
      `![CI](https://github.com/<user>/<repo>/actions/workflows/ci.yml/badge.svg)`

## 🎯 Problème résolu
Écrire manuellement des règles de validation de données pour chaque table
est répétitif et lent. Ce projet automatise cette étape avec un LLM, tout
en ajoutant une couche de détection d'anomalies par ML pour capter les
problèmes que des règles statiques ne peuvent pas voir.

## 🏗️ Architecture

```
Schema + description métier
        ↓
[1] LLM (Azure OpenAI) génère des règles SQL de validation
        ↓
[2] Rule Engine applique les règles sur les données → % conformité
        ↓
[3] ML (Isolation Forest) détecte les anomalies subtiles non couvertes
        ↓
[4] Rapport consolidé (JSON/HTML) + sauvegarde en base (historique)
        ↓
[5] Alerting (Slack) si seuil de qualité franchi
        ↓
[6] Dashboard Streamlit pour explorer les résultats
```
Le tout est orchestré par **Airflow** (exécution planifiée quotidienne) et
packagé avec **Docker Compose** (app + PostgreSQL + dashboard).

## 🛠️ Stack technique
| Composant | Technologie |
|---|---|
| LLM | Azure OpenAI |
| ML | scikit-learn (Isolation Forest) |
| Orchestration | Apache Airflow |
| Base de données | PostgreSQL + SQLAlchemy |
| Dashboard | Streamlit |
| Tests | Pytest |
| CI/CD | GitHub Actions |
| Conteneurisation | Docker / Docker Compose |

## 📁 Structure du projet
Voir l'arborescence complète dans le repo. Chaque fichier `.py` commence
par une docstring expliquant précisément son rôle et ce qu'il faut y
implémenter — utile si tu reprends le projet plus tard ou si tu veux
comprendre rapidement où intervient chaque brique.

## 🚀 Comment lancer le projet

### 1. Setup initial
```bash
git clone <ton-repo>
cd ai-data-quality-platform
cp .env .env.local   # puis remplis .env avec tes vraies valeurs (clé API, DB...)
pip install -r requirements.txt
```

### 2. Lancer avec Docker Compose (recommandé)
```bash
docker compose up --build
```
- App/pipeline : exécuté par le service `app`
- Dashboard : http://localhost:8501
- PostgreSQL : localhost:5432

### 3. Lancer manuellement (sans Docker)
```bash
python main.py                        # exécute le pipeline complet
streamlit run dashboard/app.py        # lance le dashboard
```

### 4. Lancer les tests
```bash
pytest tests/ -v --cov=src
```

## 📊 Résultat clé à mettre en avant
> "Le modèle ML a détecté **X%** d'anomalies non couvertes par les règles
> générées par le LLM" — cette métrique (calculée par
> `compare_with_rules()` dans `src/ml/anomaly_detector.py`) est LE point
> différenciant du projet à montrer en entretien : elle prouve la valeur
> ajoutée de combiner règles explicites (LLM) et détection statistique (ML).

## 🗺️ Roadmap de développement (pour toi, pas pour le README final)
1. Setup + schema + dataset
2. Génération de règles via LLM
3. Rule engine (application des règles)
4. Entraînement + détection d'anomalies ML
5. Orchestration Airflow
6. Dashboard + alerting
7. Tests + CI/CD + polish final

## 📄 Licence
MIT (ou à adapter selon ton choix)
