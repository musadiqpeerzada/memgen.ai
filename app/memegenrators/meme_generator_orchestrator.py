
from app.memegenrators.memegen_meme_generator import MemeGenLinkMemeGenerator
from app.memegenrators.openai_meme_generator import OpenAIMemeGenerator


def get_meme_generator(config):
    """Return the appropriate meme generator based on the configuration"""
    if config.meme_generator == "openai":
        return OpenAIMemeGenerator(config)
    elif config.meme_generator == "memegen":
        return MemeGenLinkMemeGenerator(config)
    else:
        raise ValueError(f"Invalid meme generator: {config.meme_generator}")