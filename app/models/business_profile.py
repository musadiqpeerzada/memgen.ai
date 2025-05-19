from pydantic import BaseModel, Field
from typing import List, Optional


class BusinessProfile(BaseModel):
    """Business profile extracted from website analysis"""
    name: str = Field(description="The business name")
    industry: str = Field(description="The primary industry the business operates in")
    core_offerings: List[str] = Field(description="Main products/services/solutions offered")
    value_propositions: List[str] = Field(description="Key differentiators and unique values")
    target_audience: List[str] = Field(description="Primary customer segments")
    brand_tone: str = Field(description="The business's tone/voice (professional, casual, etc.)")

class MemeContent(BaseModel):
    """Content for a marketing meme"""
    template_name: str = Field(description="The specific meme template to use")
    primary_text: str = Field(description="Main caption or headline for the meme")
    secondary_text: Optional[str] = Field(description="Additional text or call to action", default=None)
    hashtags: List[str] = Field(description="Relevant hashtags (without # symbol)")
    visual_description: str = Field(description="Detailed visual instructions for generating the image")
    
class MarketingCampaign(BaseModel):
    """Complete marketing meme campaign"""
    business_profile: BusinessProfile
    meme_concepts: List[MemeContent]