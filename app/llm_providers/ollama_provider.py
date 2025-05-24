from langchain_ollama import ChatOllama
from typing import Any, Dict

from app.llm_providers.base import BaseLLMProvider

class OllamaProvider(BaseLLMProvider):
    """Ollama LLM Provider"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = config.get("ollama_base_url", "http://host.docker.internal:11434")
        self.model = config.get("ollama_model", "llama3.2")
    
    def get_client(self, temperature: float = 0.7, **kwargs) -> ChatOllama:
        """Return Ollama client"""
        return ChatOllama(
            model=self.model,
            base_url=self.base_url,
            temperature=temperature,
            **kwargs
        )
    
    def get_provider_name(self) -> str:
        return "ollama"
    
    def validate_config(self) -> bool:
        """Validate Ollama configuration"""
        if not self.base_url or not self.model:
            self.logger.error("Ollama configuration missing base_url or model")
            return False
        return True