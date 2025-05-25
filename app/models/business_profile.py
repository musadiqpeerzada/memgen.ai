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
    