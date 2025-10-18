from typing import Dict, Optional
from app.services.embeddings.factory import get_embedding_generator

def generate_embeddings(content: Dict, provider: str = "openai") -> Optional[list]:
    """
    Generate embeddings for the given content using the specified provider.
    
    Args:
        content: Dictionary containing the content to generate embeddings for
        provider: The embedding provider to use (default: "openai")
        
    Returns:
        List of embeddings or None if generation fails
    """
    generator = get_embedding_generator(provider)
    return generator.create_embeddings(content)