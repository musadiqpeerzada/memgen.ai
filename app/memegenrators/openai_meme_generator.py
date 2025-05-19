import datetime
from pathlib import Path
from typing import Optional
import base64
import requests
import logging

from app.config import Config
from app.memegenrators.meme_generator_interface import MemeGeneratorInterface
from app.models.meme_content import MemeContent

logger = logging.getLogger(__name__)

class OpenAIMemeGenerator(MemeGeneratorInterface):
    """Generates images for meme concepts using DALL·E 3 via the OpenAI image generation API"""
    
    def __init__(self, config: Config):
        self.config = config
        self.save_dir = Path(getattr(config, "save_directory", "memes"))
        self.save_dir.mkdir(parents=True, exist_ok=True)
        
    def generate(self, business_name: str, meme_content: MemeContent, filename:str) -> Optional[str]:
        try:
            prompt = f"""Create a high-quality, photorealistic marketing meme for {business_name}:

Meme template to use: {meme_content.template_name}
Visual Description: {meme_content.visual_description}

Text to include:
- Main text: {meme_content.primary_text}
- Secondary text: {meme_content.secondary_text or ''}

{"- Hashtags: " + " ".join(meme_content.hashtags) if hasattr(meme_content, "hashtags") and meme_content.hashtags else ""}
"""
            logger.info(f"Generating prompt for DALL·E 3: {prompt}")
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.config.openai_api_key}"
            }
            payload = {
                "model": "dall-e-3",
                "prompt": prompt,
                "n": 1,
                "size": "1024x1024",
                "response_format": "b64_json"
            }
            
            response = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=payload)
            response.raise_for_status()
            image_response = response.json()
            
            image_data = image_response['data'][0]['b64_json']
            image_binary = base64.b64decode(image_data)
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_template_name = "".join(c if c.isalnum() else "_" for c in meme_content.template_name)
            
            with open(filename, 'wb') as file:
                file.write(image_binary)
                
            return str(filename)
            
        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            return None