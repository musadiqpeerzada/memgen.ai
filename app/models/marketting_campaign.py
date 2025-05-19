from pydantic import BaseModel, Field
from typing import List

from app.models.business_profile import BusinessProfile
from app.models.meme_content import MemeContent
    
class MarketingCampaign(BaseModel):
    """Complete marketing meme campaign"""
    business_profile: BusinessProfile
    meme_concepts: List[MemeContent]