import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
import logging

class Config:
    def __init__(self):
        load_dotenv()
        setup_logging()

        self.llm_provider = os.environ.get("LLM_PROVIDER", "ollama")
        self.ollama_base_url = os.environ.get("OLLAMA_HOST", "http://host.docker.internal:11434")
        self.ollama_model = os.environ.get("OLLAMA_MODEL", "llama3.2")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", "")
        self.meme_generator = os.environ.get("MEME_GENERATOR", "memegen")
        self.minio_base_url = os.environ.get("MINIO_BASE_URL", "http://localhost:9000")
        self.minio_access_key = os.environ.get("MINIO_ACCESS_KEY", "minioadmin")
        self.minio_secret_key = os.environ.get("MINIO_SECRET_KEY", "minioadmin")
        self.minio_bucket = os.environ.get("MINIO_BUCKET", "memgen")
        self.pinecone_api_key = os.environ.get("PINECONE_API_KEY", "")
        self.pinecone_index_name = os.environ.get("PINECONE_INDEX_NAME", "meme-templates")

    def get_llm(self, temperature=0.7):
        """Get language model based on configuration"""
        if self.llm_provider == "ollama":
            return ChatOllama(
                model=self.ollama_model,
                base_url=self.ollama_base_url,
                temperature=temperature
            )
        elif self.llm_provider == "gemeni":
            return ChatGemeni(
                model=self.gemeni_model,
                base_url=self.gemeni_base_url,
                temperature=temperature
            )
        elif self.llm_provider == "openai":
            return ChatOpenAI(
                api_key=self.openai_api_key,
                temperature=temperature
            )
        else:
            raise ValueError(f"Unknown LLM provider: {self.llm_provider}")

    def get_llm_model(self):
        """Return the appropriate model based on the config"""
        return LLModel.get_instance(self)

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

# TODO: move this to a separate file
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
