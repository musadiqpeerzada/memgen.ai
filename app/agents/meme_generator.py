from datetime import datetime
from pathlib import Path
from typing import Optional

from app.agents.agent_interface import AgentInterface
from app.config import Config
from app.memegenrators.meme_generator_orchestrator import get_meme_generator
from app.models.meme_content import MemeContent
import logging

logger = logging.getLogger(__name__)

class MemeImageGenerator(AgentInterface):
    """Generates images for meme concepts"""
    
    def __init__(self, config: Config):
        self.config = config
        self.save_dir = Path('memes')
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.generator = get_meme_generator(self.config)
        
    def do(self, business_name: str, meme_content: MemeContent) -> Optional[str]:
        """Generate a meme image from the meme content using DALL·E 3 via the OpenAI image generation API"""
        # add a timestamp to the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.save_dir/f"{business_name}_{meme_content.template_name}_{timestamp}.png"
        try:
            return self.generator.generate(business_name, meme_content, filename)
        except Exception as e:
            print(f"Error generating image: {str(e)}")
            return None
