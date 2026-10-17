import logging
import os
from typing import Optional

from dotenv import load_dotenv
from openai import AzureOpenAI, OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()

logger = logging.getLogger(__name__)


class LLMRequestError(Exception):
    pass


class LLMClient:
    def __init__(self, provider: Optional[str] = None, temperature: float = 0.1):
        self.provider = (provider or os.getenv('LLM_PROVIDER', 'azure')).lower()
        self.temperature = temperature
        if not 0 <= temperature <= 2:
            raise ValueError('temperature must be between 0 and 2')
        if self.provider == 'azure':
            self._init_azure()
        elif self.provider == 'openai':
            self._init_openai()
        else:
            raise ValueError(f'Unsupported LLM provider: {self.provider}')

    def _init_azure(self) -> None:
        api_key = os.getenv('AZURE_OPENAI_API_KEY')
        endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT')
        if not api_key:
            raise ValueError('AZURE_OPENAI_API_KEY is not configured.')
        if not endpoint:
            raise ValueError('AZURE_OPENAI_ENDPOINT is not configured.')
        if not deployment:
            raise ValueError('AZURE_OPENAI_DEPLOYMENT is not configured.')
        self.deployment = deployment
        self.client = AzureOpenAI(api_key=api_key, azure_endpoint=endpoint, api_version='2024-10-21')
        logger.info('Azure OpenAI client initialized.')

    def _init_openai(self) -> None:
        api_key = os.getenv('OPENAI_API_KEY')
        model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        if not api_key:
            raise ValueError('OPENAI_API_KEY is not configured.')
        self.model = model
        self.client = OpenAI(api_key=api_key)
        logger.info('OpenAI client initialized.')

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), reraise=True)
    def complete(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        if not prompt or not prompt.strip():
            raise ValueError('prompt cannot be empty')
        system_prompt = system_prompt or 'You are a data quality engineering expert.'
        try:
            logger.info('Sending LLM request. Prompt length=%d', len(prompt))
            if self.provider == 'azure':
                response = self.client.chat.completions.create(
                    model=self.deployment,
                    messages=[
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': prompt},
                    ],
                    temperature=self.temperature,
                )
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': prompt},
                    ],
                    temperature=self.temperature,
                )
            content = response.choices[0].message.content if response.choices else ''
            if content is None:
                content = ''
            return content.strip()
        except Exception as exc:
            logger.exception('LLM request failed')
            raise LLMRequestError(str(exc)) from exc
