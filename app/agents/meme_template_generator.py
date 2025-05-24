import json
from typing import List
from app.agents.agent_interface import AgentInterface
from app.config import Config
from app.models.business_profile import BusinessProfile
from app.models.meme_content import MemeCampaign, MemeContent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
import logging

logger = logging.getLogger(__name__)

class MemeCampaignGenerator(AgentInterface):
    """Generates creative meme marketing campaigns"""
    
    def __init__(self, config: Config):
        super().__init__(config)
        self.retry_count = 3  # Maximum number of retry attempts
        
        self.prompt = ChatPromptTemplate.from_template("""
            You are a creative marketing expert who specializes in viral meme campaigns for businesses.
            
            BUSINESS PROFILE:
            {business_profile}
            
            TASK:
            Create {num_memes} engaging marketing meme concept(s) for this business.
            
            REQUIREMENTS:
            1. Each meme should use a popular trending meme template.
            2. Relate the content to the business core offerings and value propositions.
            3. Match the brand tone ({brand_tone}) and target audience ({target_audience}).
            4. Provide a detailed visual description for image generation.
            
            FORMAT:
            Return a JSON object with a single key "memes" that maps to a JSON array of meme concepts 
            that matches the following Pydantic model for each meme:
            ```
            class MemeContent(BaseModel):
                template_name: str = Field(description="The specific meme template to use")
                primary_text: str = Field(description="Main caption or headline for the meme")
                secondary_text: Optional[str] = Field(description="Additional text or call to action", default=None)
                hashtags: List[str] = Field(description="Relevant hashtags (without # symbol)")
                visual_description: str = Field(description="Detailed visual instructions for generating the image")
            ```
            
            Return ONLY the JSON object.
        """)

        self.parser = PydanticOutputParser(pydantic_object=MemeCampaign)
        
    def do(self, business_profile: BusinessProfile, num_memes: int = 1, retry_count: int = 0) -> List[MemeContent]:
        """Generate meme concepts based on business profile
        """
        if retry_count >= self.retry_count:
            logger.error(f"Maximum retry attempts ({self.retry_count}) exceeded for {business_profile.name}")
            raise Exception(f"Failed to generate meme campaign after {self.retry_count} attempts")

        try:
            profile_json = business_profile.model_dump_json(indent=2)
            business_name = business_profile.name
            industry = business_profile.industry
            brand_tone = business_profile.brand_tone
            target_audience = ", ".join(business_profile.target_audience)
            
            logger.info(f"Generating {num_memes} meme concept(s) for {business_name}")
            
            chain = self.prompt | self.llm | self.parser
            result = chain.invoke({
                "business_profile": profile_json,
                "num_memes": num_memes,
                "business_name": business_name,
                "industry": industry,
                "brand_tone": brand_tone,
                "target_audience": target_audience
            })
            
            logger.info(f"Successfully generated meme campaign for {business_name}")
            return result.memes

        except Exception as e:
            logger.warning(f"Error generating meme campaign (attempt {retry_count + 1}/{self.retry_count}): {str(e)}")
            return self.do(business_profile, num_memes, retry_count + 1)
