from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

import logging
from app.config import Config
from app.agents.business_analyzer import BusinessAnalyzer
from app.agents.meme_generator import MemeImageGenerator
from app.agents.meme_template_generator import MemeCampaignGenerator
from app.middlewares.timeout import TimeoutMiddleware

app = FastAPI()
config = Config()

app.add_middleware(TimeoutMiddleware, timeout=60)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
rate_limit_key = f"{config.rate_limit_max_requests}/{config.rate_window}"

business_analyzer = BusinessAnalyzer(config)
meme_campaign_generator = MemeCampaignGenerator(config)
meme_generator = MemeImageGenerator(config)
logger = logging.getLogger(__name__)

@app.get("/health")
def read_root():
    return {"message": "Sab Changa si!"}

@app.post("/meme_campaign")
@limiter.limit(rate_limit_key)
def meme_campaign(request: Request, url: str, num_memes: int = 1):
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