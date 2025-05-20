from app.agents.agent_interface import AgentInterface
from app.config import Config
from app.models.business_profile import BusinessProfile
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_community.document_loaders import WebBaseLoader
import logging

logger = logging.getLogger(__name__)

class BusinessAnalyzer(AgentInterface):
    """Analyzes business websites to extract key information"""
    
    def __init__(self, config: Config):
        self.config = config
        self.llm = config.get_llm(temperature=0.2)  # Lower temperature for factual extraction
        self.character_limit = 6000
        self.retry_count = 3

        self.prompt = ChatPromptTemplate.from_template("""
            You are an expert business analyst and marketing professional.
            
            Analyze this website content and extract structured information about the business:
            
            WEBSITE CONTENT:
            {content}
            
            INSTRUCTIONS:
            Extract key business information and return it as a structured profile.
            
            1. Look for the business name, core offerings, and unique value propositions
            2. Identify their target audience/customer segments
            3. Determine the industry they operate in
            4. Pay attention to their brand tone/voice
            
            Format your response as a valid JSON object that matches this Pydantic model:
            ```
            class BusinessProfile(BaseModel):
                name: str = Field(description="The business name")
                industry: str = Field(description="The primary industry the business operates in")
                core_offerings: List[str] = Field(description="Main products/services/solutions offered")
                value_propositions: List[str] = Field(description="Key differentiators and unique values")
                target_audience: List[str] = Field(description="Primary customer segments")
                brand_tone: str = Field(description="The business's tone/voice (professional, casual, etc.)")
            ```
            
            Return ONLY the JSON object with no additional explanation or markdown formatting.
        """)
        
        self.parser = PydanticOutputParser(pydantic_object=BusinessProfile)
        
    def do(self, url: str, retry_count: int = 0, content=None) -> BusinessProfile: 
        if retry_count >= self.retry_count:
            logger.error(f"Maximum retry attempts ({self.retry_count}) exceeded for URL: {url}")
            raise Exception(f"Failed to analyze website after {self.retry_count} attempts")

        try:
            if not content:
                logger.info(f"Loading website content from: {url}")
                loader = WebBaseLoader(url)
                docs = loader.load()
                content = docs[0].page_content[:self.character_limit]

            chain = self.prompt | self.llm | self.parser
            result = chain.invoke({"content": content})
            logger.info(f"Successfully extracted business profile for: {result.name}")
            return result

        except Exception as e:
            logger.warning(
                f"Error analyzing website (attempt {retry_count + 1}/{self.retry_count}): {str(e)}"
            )
            return self.do(url, retry_count + 1, content)
