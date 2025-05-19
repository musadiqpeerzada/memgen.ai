from app.agents.business_analyzer import BusinessAnalyzer
from app.agents.meme_generator import MemeImageGenerator
from app.agents.meme_template_generator import MemeCampaignGenerator
from app.config import Config

from fastapi import FastAPI

from app.models.business_profile import BusinessProfile
from app.models.meme_content import MemeContent

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post("/analyze")
def analyze_website(url: str):
    """Analyze a website and extract business profile information"""
    config = Config()
    analyzer = BusinessAnalyzer(config)
    profile = analyzer.do(url)
    return profile

@app.post("/generate_memes")
def generate_memes(business_profile: dict, num_memes: int = 1):
    """Generate meme concepts based on business profile"""
    config = Config()
    generator = MemeCampaignGenerator(config)
    profile = BusinessProfile(**business_profile)
    memes = generator.do(profile, num_memes)
    return memes

@app.post("/generate_meme_image")
def generate_meme_image(business_name: str, meme_content: dict):
    """Generate a meme image based on the meme content"""
    config = Config()
    generator = MemeImageGenerator(config)
    content = MemeContent(**meme_content)
    image_path = generator.do(business_name, content)
    return {"image_path": image_path}