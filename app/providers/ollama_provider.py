"""
Local provider backed by Ollama.
Requires `ollama serve` running (or the in-cluster Ollama service)
and the target model already pulled, e.g.:
    ollama pull llama3.1:8b
    ollama pull nomic-embed-text
"""

import os
from typing import List

import ollama

from .base import LLMProvider


class OllamaProvider(LLMProvider):
    def __init__(
        self,
        model: str = None,
        embed_model: str = None,
        host: str = None,
    ):
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3.1:8b")
        self.embed_model = embed_model or os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
        self.host = host or os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.client = ollama.Client(host=self.host)

    @property
    def name(self) -> str:
        return "ollama"

    def generate(self, prompt: str, system: str = "", max_tokens: int = 1024) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat(
            model=self.model,
            messages=messages,
            options={"num_predict": max_tokens},
        )
        return response["message"]["content"]

    def embed(self, text: str) -> List[float]:
        response = self.client.embeddings(model=self.embed_model, prompt=text)
        return response["embedding"]
