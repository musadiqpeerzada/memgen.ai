from app.config import Config
from langchain_ollama import ChatOllama
from langchain_gemeni import ChatGemeni
from langchain_openai import ChatOpenAI

class LLModel:
    _instance = None

    def __init__(self, config: Config):
        self.config = config
        self.llm = self.config.get_llm()

    @classmethod
    def get_instance(cls, config: Config):
        if cls._instance is None:
            cls._instance = cls(config)
        return cls._instance
