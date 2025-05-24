from langchain_anthropic import ChatAnthropic
from app.llm_providers.base import BaseLLMProvider
from typing import Any, Dict

class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude LLM Provider"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("anthropic_api_key", "")
        self.model = config.get("anthropic_model", "claude-3-sonnet-20240229")
    
    def get_client(self, temperature: float = 0.7, **kwargs) -> ChatAnthropic:
        """Return Anthropic client"""
        return ChatAnthropic(
            model=self.model,
            api_key=self.api_key,
            temperature=temperature,
            **kwargs
        )
    
    def get_provider_name(self) -> str:
        return "anthropic"
    
    def validate_config(self) -> bool:
        """Validate Anthropic configuration"""
        if not self.api_key:
            self.logger.error("Anthropic API key not provided")
            return False
        return True