import logging
from typing import Dict, Optional
from openai import OpenAI
from app.config import Config
from app.services.embeddings.base import EmbeddingGenerator

logger = logging.getLogger(__name__)

class OpenAIEmbeddingGenerator(EmbeddingGenerator):
    def __init__(self, config: Config):
        api_key = config.llm_config.get('openai_api_key')
        if not api_key:
            raise ValueError("OpenAI API key not found in configuration")
        self.client = OpenAI(api_key=api_key)
        
    def create_embeddings(self, content: Dict) -> Optional[list]:
        """Generate embeddings using OpenAI's API"""
        content_text = " ".join(str(value) for value in content.values() if value)
        if not content_text.strip():
            logger.warning("Content text is empty.")
            return None
            
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=content_text,
                dimensions=384
            )
            if not response or not response.data:
                logger.error("Embedding generation failed.")
                return None
            return response.data[0].embedding
        except Exception as e:
            logger.exception(f"Failed to generate embedding: {e}")
            return None