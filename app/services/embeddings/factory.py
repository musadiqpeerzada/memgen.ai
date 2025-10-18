from typing import Optional, Type
from app.config import Config
from app.services.embeddings.base import EmbeddingGenerator
from app.services.embeddings.openai_embeddings import OpenAIEmbeddingGenerator

EMBEDDING_PROVIDERS = {
    "openai": OpenAIEmbeddingGenerator
}

def get_embedding_generator(provider: str = "openai", config: Optional[Config] = None) -> EmbeddingGenerator:
    """Factory function to get the appropriate embedding generator"""
    if config is None:
        config = Config()
        
    if provider not in EMBEDDING_PROVIDERS:
        raise ValueError(f"Unsupported embedding provider: {provider}")
        
    generator_class: Type[EmbeddingGenerator] = EMBEDDING_PROVIDERS[provider]
    return generator_class(config)