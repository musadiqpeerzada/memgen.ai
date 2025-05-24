import os
from dotenv import load_dotenv
import logging

from app.llm_providers.base import BaseLLMProvider
from app.llm_providers.factory import LLMProviderFactory

class Config:
    def __init__(self):
        load_dotenv()
        self._setup_logging()

        self.llm_provider_name = os.environ.get("LLM_PROVIDER", "gemini")
        self.llm_config = self._build_llm_config()
        
        self.llm_provider = LLMProviderFactory.create_provider(
            self.llm_provider_name, 
            self.llm_config
        )
        
        self.meme_generator = os.environ.get("MEME_GENERATOR", "memegen")
        self.minio_base_url = os.environ.get("MINIO_BASE_URL", "http://localhost:9000")
        self.minio_access_key = os.environ.get("MINIO_ACCESS_KEY", "minioadmin")
        self.minio_secret_key = os.environ.get("MINIO_SECRET_KEY", "minioadmin")
        self.minio_bucket = os.environ.get("MINIO_BUCKET", "memgen")
        self.pinecone_api_key = os.environ.get("PINECONE_API_KEY", "")
        self.pinecone_index_name = os.environ.get("PINECONE_INDEX_NAME", "meme-templates")

    def _build_llm_config(self) -> dict:
        return {
            # Ollama config
            "ollama_base_url": os.environ.get("OLLAMA_HOST", "http://host.docker.internal:11434"),
            "ollama_model": os.environ.get("OLLAMA_MODEL", "llama3.2"),
            
            # OpenAI config
            "openai_api_key": os.environ.get("OPENAI_API_KEY", ""),
            "openai_model": os.environ.get("OPENAI_MODEL", "gpt-4"),
            
            # Anthropic config
            "anthropic_api_key": os.environ.get("ANTHROPIC_API_KEY", ""),
            "anthropic_model": os.environ.get("ANTHROPIC_MODEL", "claude-3-sonnet-20240229"),
            
            # Google Gemini config
            "google_api_key": os.environ.get("GOOGLE_API_KEY", ""),
            "gemini_model": os.environ.get("GEMINI_MODEL", "gemini-2.0-flash"),
        }

    def get_llm(self, temperature: float = 0.7, **kwargs):
        """Get language model instance"""
        return self.llm_provider.get_client(temperature=temperature, **kwargs)
    
    def get_llm_provider(self) -> BaseLLMProvider:
        """Get the LLM provider instance"""
        return self.llm_provider
    
    def get_available_llm_providers(self) -> list:
        """Get list of available LLM providers"""
        return LLMProviderFactory.get_available_providers()

    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )