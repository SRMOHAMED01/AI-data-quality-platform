"""
connection.py
===============

RÔLE DE CE FICHIER
-------------------
Centraliser la connexion à la base PostgreSQL : créer le moteur
SQLAlchemy (`engine`), la session, et exposer `Base` (utilisée par
models.py pour définir les tables).

CE QU'IL FAUT IMPLÉMENTER
--------------------------
1. Charger l'URL de connexion depuis `.env` :
       DATABASE_URL=postgresql://user:password@localhost:5432/dataquality

2. Créer :
   - `engine = create_engine(DATABASE_URL)`
   - `SessionLocal = sessionmaker(bind=engine)`
   - `Base = declarative_base()`

3. Une fonction `init_db()` qui crée toutes les tables si elles
   n'existent pas encore :
       Base.metadata.create_all(bind=engine)
   (à appeler une fois au démarrage de l'app / dans un script setup.py)

4. Une fonction `get_session()` (context manager ou générateur) qui
   ouvre une session, la retourne, et la ferme proprement après usage
   (pattern classique SQLAlchemy) :
       @contextmanager
       def get_session():
           session = SessionLocal()
           try:
               yield session
               session.commit()
           except Exception:
               session.rollback()
               raise
           finally:
               session.close()

POINTS D'ATTENTION
-------------------
- Ne jamais mettre le mot de passe DB en dur dans le code — toujours via
  `.env`.
- En Docker Compose, le host ne sera pas `localhost` mais le nom du
  service Postgres défini dans docker-compose.yml (ex: `db`).
"""

# TODO: import os, from dotenv import load_dotenv
# TODO: from sqlalchemy import create_engine
# TODO: from sqlalchemy.orm import sessionmaker, declarative_base
# TODO: implémenter engine, SessionLocal, Base, init_db(), get_session()
