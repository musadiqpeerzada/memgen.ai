from app.agents.business_analyzer import BusinessAnalyzer
from app.config import Config

from fastapi import FastAPI

from app.models.business_profile import BusinessProfile

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
