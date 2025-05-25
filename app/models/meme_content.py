from pydantic import BaseModel, Field
from typing import List, Optional

from typing import List
from pydantic import BaseModel, Field

class MemeContent(BaseModel):
    """Content for a marketing meme"""
    template_name: str = Field(description="The specific meme template to use")
    texts: List[str] = Field(description="Text components to be placed on the meme, ordered as required by the template")
    hashtags: List[str] = Field(description="Relevant hashtags (without # symbol)")
    visual_description: str = Field(description="Detailed visual instructions for generating the image")

class MemeCampaign(BaseModel):
    memes: List[MemeContent] = Field(..., description="List of generated meme concepts")