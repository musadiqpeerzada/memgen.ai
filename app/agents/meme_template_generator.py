import json
from typing import List
from app.agents.agent_interface import AgentInterface
from app.config import Config
from app.models.business_profile import BusinessProfile
from app.models.meme_content import MemeCampaign, MemeContent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
import logging

from app.services.pinecone import PineconeClient

logger = logging.getLogger(__name__)

class MemeCampaignGenerator(AgentInterface):
    """Generates creative meme marketing campaigns"""
    
    def __init__(self, config: Config):
        self.config = config
        self.llm = config.get_llm(temperature=1.2)
        self.retry_count = 3
        self.llm_provider = config.get_llm_provider()
        self.pinecone_client = PineconeClient(config)
        self.prompt = ChatPromptTemplate.from_template("""
           You are a viral marketing expert who creates memes that actually get shared and saved. 
            You understand internet culture, current trends, and what makes content relatable to real people.
            
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
            Create {num_memes} VIRAL-WORTHY meme concept(s) that people will actually want to share, save, and relate to.
            
            CREATIVITY REQUIREMENTS:
            1. Research and use CURRENT viral meme templates that are trending and recognizable
            2. Connect business value to GENUINE pain points people experience daily
            3. Make it ACTUALLY funny or relatable, not corporate-cringe
            4. Use language and references your target audience naturally uses
            5. Address real problems with humor, not generic business speak
            6. Tap into current cultural moments, trending topics, and internet culture
            7. Make people think "this is so me" or "I need to send this to my friend"
            8. Use authentic generational language (Gen Z slang, millennial references, etc.)
            9. Reference current events, social trends, or shared cultural experiences
            10. Think like someone who spends time on TikTok, Instagram, Twitter, and Reddit
            
            RELATABILITY CHECKLIST:
            - Does this sound like something a real person would say?
            - Would someone screenshot this and send it in a group chat?
            - Does it acknowledge a real struggle or universal experience?
            - Is the humor authentic to the demographic?
            - Does it feel timely and current?
            - Does it use meme formats people actually recognize and share?
            - Would this get engagement (likes, shares, saves) on social media?
            
            RESEARCH APPROACH:
            - Think about what's currently trending in meme culture
            - Consider what pain points the target audience faces RIGHT NOW
            - Use your knowledge of internet culture and social media trends
            - Draw from current events, generational experiences, and shared struggles
            - Consider platform-specific humor (TikTok vs Instagram vs Twitter style)
            
            FORMAT INSTRUCTIONS:
            For each meme:
            - Choose a viral, recognizable meme template that fits the message
            - Create content that uses the template format correctly
            - Connect naturally to business value without being obviously promotional
            - Use authentic language that matches the target demographic
            - Include current references or trending topics when relevant
            
            FORMAT:
            Return a JSON object with a single key "memes" that maps to a JSON array of meme concepts 
            that matches the following Pydantic model for each meme:
            ```
            class MemeContent(BaseModel):
                template_name: str = Field(description="The specific meme template to use")
                texts: List[str] = Field(description="Text components to be placed on the meme, ordered as required by the template")
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
            logger.info(f"Generating {num_memes} meme concept(s) for {name}"f" using {provider_name} provider")
            
            chain = self.prompt | self.llm | self.parser
            result = chain.invoke({
                "name": name,
                "industry": industry,
                "core_offerings": core_offerings,
                "value_propositions": value_propositions,
                "target_audience": target_audience,
                "brand_tone": brand_tone,
                "num_memes": num_memes,
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