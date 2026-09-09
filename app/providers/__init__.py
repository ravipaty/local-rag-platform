from .base import LLMProvider


def get_provider(name: str = None) -> LLMProvider:
    """
    Factory: returns the configured provider.
    Controlled by LLM_PROVIDER env var — defaults to 'ollama'.
    """
    import os

    provider_name = (name or os.getenv("LLM_PROVIDER", "ollama")).lower()

    if provider_name == "ollama":
        from .ollama_provider import OllamaProvider
        return OllamaProvider()
    elif provider_name == "bedrock":
        from .bedrock_provider import BedrockProvider
        return BedrockProvider()
    else:
        raise ValueError(f"Unknown LLM_PROVIDER: {provider_name}")
