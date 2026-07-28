# Dockerfile
# ============
#
# RÔLE DE CE FICHIER
# -------------------
# Construire l'image Docker de l'application Python (contient tout le
# code src/, les dépendances, et lance main.py par défaut).
#
# CE QU'IL FAUT IMPLÉMENTER
# --------------------------
# 1. Partir d'une image de base légère : `python:3.11-slim`
# 2. Définir `WORKDIR /app`
# 3. Copier `requirements.txt` en premier et installer les dépendances
#    (AVANT de copier tout le code) — ça permet à Docker de mettre en
#    cache la couche d'installation des dépendances, et de ne pas tout
#    réinstaller à chaque petit changement de code.
# 4. Copier le reste du code (`COPY . .`)
# 5. Définir la commande par défaut : `CMD ["python", "main.py"]`
#    (le service `dashboard` dans docker-compose.yml overridera cette
#    commande avec `streamlit run ...`)
#
# SQUELETTE À COMPLÉTER (structure attendue)
# ----------------------------------------------
# FROM python:3.11-slim
#
# WORKDIR /app
#
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
#
# COPY . .
#
# CMD ["python", "main.py"]
#
# POINTS D'ATTENTION
# -------------------
# - Ajoute un `.dockerignore` (voir fichier séparé) pour ne pas copier
#   les fichiers inutiles (venv, .git, __pycache__, data volumineuses)
#   dans l'image — ça la rend plus légère et le build plus rapide.
