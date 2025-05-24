from typing import Dict, Any

from app.llm_providers.anthropic_provider import AnthropicProvider
from app.llm_providers.gemini_provider import GeminiProvider
from app.llm_providers.ollama_provider import OllamaProvider
from app.llm_providers.openai_provider import OpenAIProvider
from .base import BaseLLMProvider
import logging

logger = logging.getLogger(__name__)

class LLMProviderFactory:
    """Factory for creating LLM providers"""
    
    _providers = {
        "ollama": OllamaProvider,
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "gemini": GeminiProvider,
    }
    
    @classmethod
    def create_provider(cls, provider_name: str, config: Dict[str, Any]) -> BaseLLMProvider:
        """Create an LLM provider instance"""
        if provider_name not in cls._providers:
            available = ", ".join(cls._providers.keys())
            raise ValueError(f"Unknown LLM provider: {provider_name}. Available: {available}")
        
        provider_class = cls._providers[provider_name]
        provider = provider_class(config)
        
        if not provider.validate_config():
            raise ValueError(f"Invalid configuration for {provider_name} provider")
        
        logger.info(f"Created {provider_name} LLM provider")
        return provider
    
    @classmethod
    def get_available_providers(cls) -> list:
        """Get list of available providers"""
        return list(cls._providers.keys())
