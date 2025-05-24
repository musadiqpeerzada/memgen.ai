from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logger
    
    @abstractmethod
    def get_client(self, temperature: float = 0.7, **kwargs) -> Any:
        """Return the LLM client instance"""
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Return the name of the LLM provider"""
        pass
    
    def validate_config(self) -> bool:
        """Validate provider-specific configuration"""
        return True
