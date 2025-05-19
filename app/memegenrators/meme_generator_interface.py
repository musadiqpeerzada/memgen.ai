from abc import ABC, abstractmethod
from typing import Optional
from app.models.meme_content import MemeContent


class MemeGeneratorInterface(ABC):
    @abstractmethod
    def generate(self, business_name: str, meme_content: MemeContent, filename: str) -> Optional[str]:
        """Generate a meme image from the provided meme content."""
        pass
