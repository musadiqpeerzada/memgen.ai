import os
from io import BytesIO
from pathlib import Path
from typing import Optional, Dict
import requests
import logging
import numpy as np
from sentence_transformers import SentenceTransformer
from app.config import Config
from app.memegenrators.meme_generator_interface import MemeGeneratorInterface
from app.models.meme_content import MemeContent
from app.services.minio import MinioClient
from app.services.pinecone import PineconeClient

logger = logging.getLogger(__name__)

class MemeGenLinkMemeGenerator(MemeGeneratorInterface):
    """Generates images using the memegen.link API"""

    def __init__(self, config: Config):
        self.config = config
        self.save_dir = Path(getattr(config, "save_directory", "memes"))
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.minio_client = MinioClient(config)
        self.pinecone_client = PineconeClient(config)

    def generate(self, business_name: str, meme_content: MemeContent, filename: str) -> Optional[str]:
        try:
            related_template = self.find_related_template(meme_content)
            if not related_template:
                logger.warning("No related template found.")
                return None
            template_id = related_template.get("id", "")
            top_text = meme_content.primary_text.strip()
            bottom_text = (meme_content.secondary_text or "").strip()
            # Build the memegen URL
            url = f"https://api.memegen.link/images/{template_id}/{top_text}/{bottom_text}.png"
            logger.info(f"Fetching meme URL: {url}")
            image_response = requests.get(url=url)
            image_bytes = image_response.content
            image_stream = BytesIO(image_bytes)
            object_name = Path(filename).name
            presigned_url = self.minio_client.put_file(image_stream, object_name)
            logger.info(f"Meme saved to {presigned_url}")
            return presigned_url
        except Exception as e:
            logger.error(f"Error generating image with Memegen API: {str(e)}")
            return None

    def find_related_template(self, meme_content: MemeContent) -> Optional[Dict]:
        content_text = (
            f"{meme_content.template_name}. "
            f"{meme_content.primary_text} "
            f"{meme_content.secondary_text or ''} "
            f"{meme_content.visual_description}"
        )
        if not content_text.strip():
            logger.warning("Content text is empty.")
            return None

        query_embedding = self.model.encode(content_text, convert_to_numpy=True).tolist()
        if not query_embedding or not isinstance(query_embedding, list):
            logger.error("Embedding generation failed.")
            return None

        try:
            query_response = self.pinecone_client.query(
                query_vector=query_embedding,
            )
        except Exception as e:
            logger.exception(f"Failed to query Pinecone: {e}")
            return None

        matches = query_response.get("matches", [])
        if matches:
            return {
                "id": matches[0]["id"],
                "name": matches[0]["metadata"].get("name", "")
            }

        logger.info("No match found.")
        return None
