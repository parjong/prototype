import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import ollama

logger = logging.getLogger(__name__)


class InferenceAdapter(ABC):
    @abstractmethod
    async def chat(
        self, messages: List[Dict[str, str]], options: Optional[Dict[str, Any]] = None
    ) -> str:
        pass

    @abstractmethod
    async def embed(self, text: str) -> List[float]:
        pass


class OllamaAdapter(InferenceAdapter):
    def __init__(self, model_name: str, base_url: Optional[str] = None):
        self.model_name = model_name
        self.client = ollama.AsyncClient(host=base_url)

    async def chat(
        self, messages: List[Dict[str, str]], options: Optional[Dict[str, Any]] = None
    ) -> str:
        try:
            response = await self.client.chat(
                model=self.model_name,
                messages=messages,
                options=options or {},
            )
            return response["message"]["content"]
        except Exception as e:
            logger.error(f"Ollama chat error: {e}")
            raise

    async def embed(self, text: str) -> List[float]:
        try:
            response = await self.client.embed(
                model=self.model_name,
                input=text,
            )
            return response["embeddings"][0]
        except Exception as e:
            logger.error(f"Ollama embedding error: {e}")
            raise
