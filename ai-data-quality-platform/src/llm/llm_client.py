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

import logging
import os
from typing import Optional

from dotenv import load_dotenv
from openai import AzureOpenAI, OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential


load_dotenv()

logger = logging.getLogger(__name__)


class LLMRequestError(Exception):
    """Raised when an LLM request fails."""


class LLMClient:
    """
    Centralized client for OpenAI and Azure OpenAI.

    This is the only module in the application that communicates
    directly with an LLM provider.
    """

    def __init__(
        self,
        provider: Optional[str] = None,
        temperature: float = 0.1,
    ):
        self.provider = (
            provider or os.getenv("LLM_PROVIDER", "azure")
        ).lower()

        self.temperature = temperature

        if not 0 <= temperature <= 2:
            raise ValueError("temperature must be between 0 and 2")

        if self.provider == "azure":
            self._init_azure()

        elif self.provider == "openai":
            self._init_openai()

        else:
            raise ValueError(
                f"Unsupported LLM provider: {self.provider}"
            )

    def _init_azure(self) -> None:
        """Initialize Azure OpenAI client."""

        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

        if not api_key:
            raise ValueError(
                "AZURE_OPENAI_API_KEY is not configured."
            )

        if not endpoint:
            raise ValueError(
                "AZURE_OPENAI_ENDPOINT is not configured."
            )

        if not deployment:
            raise ValueError(
                "AZURE_OPENAI_DEPLOYMENT is not configured."
            )

        self.deployment = deployment

        self.client = AzureOpenAI(
            api_key=api_key,
            azure_endpoint=endpoint,
            api_version="2024-10-21",
        )

        logger.info("Azure OpenAI client initialized.")

    def _init_openai(self) -> None:
        """Initialize direct OpenAI client."""

        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is not configured."
            )

        self.model = model

        self.client = OpenAI(
            api_key=api_key,
        )

        logger.info("OpenAI client initialized.")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(
            multiplier=1,
            min=2,
            max=10,
        ),
        reraise=True,
    )
    def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> str:
        """
        Send a prompt to the configured LLM provider.

        Retries transient API failures up to three times.
        """

        if not prompt or not prompt.strip():
            raise ValueError("prompt cannot be empty")

        system_prompt = system_prompt or (
            "You are a data quality engineering expert."
        )

        try:
            logger.info(
                "Sending LLM request. Prompt length=%d",
                len(prompt),
            )

            if self.provider == "azure":
                response = self.client.chat.completions.create(
                    model=self.deployment,
                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt,
                        },
                        {
                            "role": "user",
                            "content": prompt,
                        },
                    ],
                    temperature=self.temperature,
                )

            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt,
                        },
                        {
                            "role": "user",
                            "content": prompt,
                        },
                    ],
                    temperature=self.temperature,
                )

            content = response.choices[0].message.content

            if not content:
                raise LLMRequestError(
                    "LLM returned an empty response."
                )

            logger.info("LLM request completed successfully.")

            return content.strip()

        except Exception as exc:
            logger.exception("LLM request failed.")
            raise LLMRequestError(
                f"LLM request failed: {exc}"
            ) from exc