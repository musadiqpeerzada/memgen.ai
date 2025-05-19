import datetime
from pathlib import Path
from typing import Dict, List, Optional
import requests
import logging
import numpy as np
from sentence_transformers import SentenceTransformer

from app.config import Config
from app.memegenrators.meme_generator_interface import MemeGeneratorInterface
from app.models.meme_content import MemeContent
from app.utils import fetch_meme_templates

logger = logging.getLogger(__name__)

class MemeGenLinkMemeGenerator(MemeGeneratorInterface):
    """Generates images using the memegen.link API"""
    
    def __init__(self, config: Config):
        self.config = config
        self.save_dir = Path(getattr(config, "save_directory", "memes"))
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def generate(self, business_name: str, meme_content: MemeContent, filename: str) -> Optional[str]:
        try:
            templates = fetch_meme_templates()
            if not templates:
                logger.warning("No meme templates found.")
                return None
            related_template = self.find_related_template(templates, meme_content)
            if not related_template:
                logger.warning("No related template found.")
                return None
            template_id = related_template.get("id", "")
            
            top_text = meme_content.primary_text.strip()
            bottom_text = (meme_content.secondary_text or "").strip()
            
            # Build the memegen URL
            url = f"https://api.memegen.link/images/{template_id}/{top_text}/{bottom_text}.png"
            print(url)
            
            image_response = requests.get(url=url)
            with open(filename, "wb") as f:
                f.write(image_response.content)

            
            print(f"Meme saved to {filename}")
            return str(filename)
        except Exception as e:
            logger.error(f"Error generating image with Memegen API: {str(e)}")
            return None

    def find_related_template(self, templates: List[Dict], meme_content) -> Optional[Dict]:
        content_text = (
            f"{meme_content.template_name}. "
            f"{meme_content.primary_text} "
            f"{meme_content.secondary_text or ''} "
            f"{meme_content.visual_description}"
        )

        content_embedding = self.get_embedding(content_text)
        similarities = []

        for template in templates:
            template_name = template.get("name", "")
            template_embedding = self.get_embedding(template_name)
            sim = cosine_similarity(content_embedding, template_embedding)
            similarities.append((template, sim))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[0][0] if similarities else None

    def get_embedding(self, text: str) -> np.ndarray:
        return self.model.encode(text, convert_to_numpy=True)

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    norm_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    if norm_product == 0:
        return 0.0
    return np.dot(vec1, vec2) / norm_product
