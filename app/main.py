from fastapi import FastAPI
import logging
from app.config import Config
from app.agents.business_analyzer import BusinessAnalyzer
from app.agents.meme_generator import MemeImageGenerator
from app.agents.meme_template_generator import MemeCampaignGenerator
from app.models.business_profile import BusinessProfile
from app.models.meme_content import MemeContent

app = FastAPI()
config = Config()
business_analyzer = BusinessAnalyzer(config)
meme_campaign_generator = MemeCampaignGenerator(config)
meme_generator = MemeImageGenerator(config)
logger = logging.getLogger(__name__)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post("/analyze")
def analyze_website(url: str):
    """Analyze a website and extract business profile information"""
    profile = business_analyzer.do(url)
    return profile

@app.post("/generate_memes")
def generate_memes(business_profile: dict, num_memes: int = 1):
    """Generate meme concepts based on business profile"""
    profile = BusinessProfile(**business_profile)
    memes = meme_campaign_generator.do(profile, num_memes)
    return memes

@app.post("/generate_meme_image")
def generate_meme_image(business_name: str, meme_content: dict):
    """Generate a meme image based on the meme content"""
    content = MemeContent(**meme_content)
    image_path = meme_generator.do(business_name, content)
    return {"image_path": image_path}

@app.post("/meme_campaign")
def meme_campaign(url: str, num_memes: int = 1):
    """Generate a meme campaign based on a website"""
    business_profile = business_analyzer.do(url)
    logger.info(f"Business profile: {business_profile}")   
    meme_content = meme_campaign_generator.do(business_profile, num_memes)
    logger.info(f"Generated meme content: {meme_content}")
    meme_images = []
    for meme in meme_content:
        image_path = meme_generator.do(business_profile.name, meme)
        meme_images.append(image_path)
    return {"meme_images": meme_images}