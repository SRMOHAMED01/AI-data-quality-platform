"""
llm_client.py
==============

RÔLE DE CE FICHIER
-------------------
Ce module est le SEUL endroit du projet qui parle directement à l'API du
LLM (OpenAI ou Azure OpenAI). Tout le reste du code passe par lui — ça
permet de changer de fournisseur LLM (OpenAI -> Azure OpenAI -> Mistral)
sans toucher au reste du projet.

CE QU'IL FAUT IMPLÉMENTER
--------------------------
1. Une classe `LLMClient` avec :
   - `__init__`: charge la clé API depuis les variables d'environnement
     (via python-dotenv), configure le client (openai.OpenAI(...) ou
     AzureOpenAI(...) selon le provider).
   - `complete(prompt: str, system_prompt: str = None) -> str`:
     envoie le prompt au modèle, retourne la réponse texte brute.
   - Ajouter un `try/except` pour capturer les erreurs réseau/API et
     lever une exception custom (ex: `LLMRequestError`).

2. Gérer le retry en cas d'échec (ex: avec la lib `tenacity`) — un appel
   API peut timeout ou renvoyer une erreur 429 (rate limit).

3. Ne jamais hardcoder la clé API : elle doit venir de `.env` via
   `os.getenv("AZURE_OPENAI_API_KEY")`.

VARIABLES D'ENVIRONNEMENT ATTENDUES (à mettre dans .env)
----------------------------------------------------------
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_DEPLOYMENT=...
# ou si tu utilises OpenAI directement :
OPENAI_API_KEY=...

EXEMPLE D'UTILISATION ATTENDU (par les autres fichiers)
----------------------------------------------------------
    from src.llm.llm_client import LLMClient

    client = LLMClient()
    response = client.complete(prompt="...", system_prompt="Tu es un expert en qualité de données.")

POINTS D'ATTENTION
-------------------
- Loggue chaque appel (prompt tronqué + tokens utilisés) pour pouvoir
  débugger / suivre les coûts.
- Ajoute un paramètre `temperature` bas (0 à 0.2) car on veut des règles
  déterministes, pas créatives.
"""

# TODO: import os, from dotenv import load_dotenv, import openai (ou AzureOpenAI)
# TODO: implémenter la classe LLMClient décrite ci-dessus
