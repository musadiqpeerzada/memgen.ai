from app.llm_providers.base import BaseLLMProvider
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Any, Dict
class GeminiProvider(BaseLLMProvider):
    """Google Gemini LLM Provider"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("google_api_key", "")
        self.model = config.get("gemini_model", "gemini-1.5-pro")
    
    def get_client(self, temperature: float = 0.7, **kwargs) -> ChatGoogleGenerativeAI:
        """Return Gemini client"""
        return ChatGoogleGenerativeAI(
            model=self.model,
            google_api_key=self.api_key,
            temperature=temperature,
            **kwargs
        )
    
    def get_provider_name(self) -> str:
        return "gemini"
    
    def validate_config(self) -> bool:
        """Validate Gemini configuration"""
        if not self.api_key:
            self.logger.error("Google API key not provided")
            return False
        return True
