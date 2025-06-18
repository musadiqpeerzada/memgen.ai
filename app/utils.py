import json
import os
import requests
import logging
from typing import Dict, Optional
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)
encoding_model = SentenceTransformer('models/all-MiniLM-L6-v2')

def fetch_meme_templates():
    try:
        # Check if the file exists and is not empty
        if os.path.exists("templates.json") and os.path.getsize("templates.json") > 0:
            with open("templates.json", "r") as file:
                return json.load(file)
        response = requests.get("https://api.memegen.link/templates")
        if response.status_code == 200:
            # write the response to a file
            with open("templates.json", "w") as file:
                file.write(response.text)
            return response.json()
        return []
    except Exception as e:
        print(f"Error fetching templates: {e}")
        return []

def create_embeddings(content: Dict) -> Optional[list]:
    content_text = " ".join(str(value) for value in content.values() if value)
    if not content_text.strip():
        logger.warning("Content text is empty.")
        return None
    try:
        query_embedding = encoding_model.encode(content_text, convert_to_numpy=True).tolist()
        if not query_embedding or not isinstance(query_embedding, list):
            logger.error("Embedding generation failed.")
            return None   
        return query_embedding
    except Exception as e:
        logger.exception(f"Failed to generate embedding: {e}")
        return None
    