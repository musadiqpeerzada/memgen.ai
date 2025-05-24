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
        self.config = config
        self.llm = config.get_llm(temperature=0.8)
        self.retry_count = 3
        self.llm_provider = config.get_llm_provider()
        
        self.prompt = ChatPromptTemplate.from_template("""
            You are a creative marketing expert who specializes in viral meme campaigns for businesses.
            
            BUSINESS PROFILE:
            Name: {name}
            Industry: {industry}
            
            Core Offerings:
            {core_offerings}
            
            Value Propositions:
            {value_propositions}
            
            Target Audience:
            {target_audience}
            
            Brand Tone: {brand_tone}
            
            TASK:
            Create {num_memes} engaging marketing meme concept(s) for this business.
            
            REQUIREMENTS:
            1. Each meme should use a popular trending meme template.
            2. Relate the content to the business core offerings and value propositions.
            3. Match the brand tone and target the specified audience segments.
            4. Provide a detailed visual description for image generation.
            5. Focus on financial wellness, employee benefits, and modern workplace themes.
            
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
        provider_name = self.llm_provider.get_provider_name()
        if retry_count >= self.retry_count:
            logger.error(
                f"Maximum retry attempts ({self.retry_count}) exceeded for {business_profile.name} "
                f"using {provider_name} provider"
            )
            raise Exception(f"Failed to generate meme campaign after {self.retry_count} attempts")

        try:
            name = business_profile.name
            industry = business_profile.industry
            core_offerings = "\n".join([f"• {offering}" for offering in business_profile.core_offerings])
            value_propositions = "\n".join([f"• {prop}" for prop in business_profile.value_propositions])
            target_audience = "\n".join([f"• {audience}" for audience in business_profile.target_audience])
            brand_tone = business_profile.brand_tone
            
            logger.info(f"Generating {num_memes} meme concept(s) for {name}"f"using {provider_name} provider")
            
            chain = self.prompt | self.llm | self.parser
            result = chain.invoke({
                "name": name,
                "industry": industry,
                "core_offerings": core_offerings,
                "value_propositions": value_propositions,
                "target_audience": target_audience,
                "brand_tone": brand_tone,
                "num_memes": num_memes
            })
            
            logger.info(
                f"Successfully generated {len(result.memes)} meme concept(s) for {name} "
                f"using {provider_name} provider"
            )
            return result.memes

        except Exception as e:
            logger.warning(f"Error generating meme campaign using {provider_name} "
            f"(attempt {retry_count + 1}/{self.retry_count}): {str(e)}")
            return self.do(business_profile, num_memes, retry_count + 1)
