from pydantic import BaseModel, Field
from typing import List, Optional

class MemeContent(BaseModel):
    """Content for a marketing meme"""
    template_name: str = Field(description="The specific meme template to use")
    primary_text: str = Field(description="Main caption or headline for the meme")
    secondary_text: Optional[str] = Field(description="Additional text or call to action", default=None)
    hashtags: List[str] = Field(description="Relevant hashtags (without # symbol)")
    visual_description: str = Field(description="Detailed visual instructions for generating the image")

class MemeCampaign(BaseModel):
    memes: List[MemeContent] = Field(..., description="List of generated meme concepts")