from langchain_openai import ChatOpenAI
from app.llm_providers.base import BaseLLMProvider
from typing import Any, Dict

class OpenAIProvider(BaseLLMProvider):
    """OpenAI LLM Provider"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("openai_api_key", "")
        self.model = config.get("openai_model", "gpt-4")
    
    def get_client(self, temperature: float = 0.7, **kwargs) -> ChatOpenAI:
        """Return OpenAI client"""
        return ChatOpenAI(
            model=self.model,
            api_key=self.api_key,
            temperature=temperature,
            **kwargs
        )
    
    def get_provider_name(self) -> str:
        return "openai"
    
    def validate_config(self) -> bool:
        """Validate OpenAI configuration"""
        if not self.api_key:
            self.logger.error("OpenAI API key not provided")
            return False
        return True
