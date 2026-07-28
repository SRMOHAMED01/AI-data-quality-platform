"""
models.py
==========

RÔLE DE CE FICHIER
-------------------
Définir les modèles SQLAlchemy (ORM) qui représentent les tables de la
base PostgreSQL utilisée par le projet : la table de transactions brutes,
et une table pour stocker l'historique des exécutions de qualité (runs).

CE QU'IL FAUT IMPLÉMENTER
--------------------------
1. Une classe `Transaction(Base)` mappant la table `transactions` :
   colonnes : id, amount, email, transaction_date, status, country
   (mêmes colonnes que dans schema/table_schema.json).

2. Une classe `QualityRun(Base)` mappant une table `quality_runs`, qui
   sert d'historique : à chaque exécution du pipeline, on enregistre
   - run_id (UUID ou auto-increment)
   - timestamp d'exécution
   - nombre de règles appliquées
   - % de conformité global
   - nombre d'anomalies ML détectées
   - statut (success/failed)
   Ça permet d'avoir un historique consultable dans le dashboard
   ("évolution de la qualité des données dans le temps").

3. Une classe `RuleResult(Base)` mappant une table `rule_results` liée à
   `QualityRun` (clé étrangère `run_id`) : stocke le résultat détaillé de
   chaque règle pour chaque run (colonne, règle, % conformité, sévérité).

EXEMPLE DE STRUCTURE ATTENDUE
--------------------------------
    class Transaction(Base):
        __tablename__ = "transactions"
        id = Column(Integer, primary_key=True)
        amount = Column(Float)
        email = Column(String)
        transaction_date = Column(Date)
        status = Column(String)
        country = Column(String)

POINTS D'ATTENTION
-------------------
- Utiliser `Base = declarative_base()` importé depuis `connection.py`
  pour éviter les imports circulaires.
- Ajouter des `Index` sur les colonnes souvent filtrées (transaction_date,
  status) pour des perfs correctes si le volume grossit.
"""

# TODO: from sqlalchemy import Column, Integer, Float, String, Date, DateTime, ForeignKey
# TODO: from src.db.connection import Base
# TODO: implémenter Transaction, QualityRun, RuleResult
