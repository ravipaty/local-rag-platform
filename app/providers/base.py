"""
Abstract interface that every LLM provider must implement.
This lets query.py / ingest.py stay provider-agnostic — swap
Ollama for Bedrock (or anything else) by changing one env var.
"""

from abc import ABC, abstractmethod
from typing import List


class LLMProvider(ABC):
    """Common interface for local or cloud LLM providers."""

    @abstractmethod
    def generate(self, prompt: str, system: str = "", max_tokens: int = 1024) -> str:
        """Send a prompt to the model and return the text completion."""
        raise NotImplementedError

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """Return an embedding vector for the given text."""
        raise NotImplementedError

    @property
    @abstractmethod
    def name(self) -> str:
        """Short identifier for logging/tracing (e.g. 'ollama', 'bedrock')."""
        raise NotImplementedError
