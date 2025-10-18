from typing import Dict, Optional, Protocol
from abc import ABC, abstractmethod

class EmbeddingGenerator(Protocol):
    """Protocol for embedding generators"""
    def create_embeddings(self, content: Dict) -> Optional[list]:
        """Generate embeddings for the given content"""
        pass