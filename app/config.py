import os
from pathlib import Path
from langchain_ollama import ChatOllama
import logging

class Config:
    def __init__(self):
        self.llm_provider = os.environ.get("LLM_PROVIDER", "ollama")
        self.ollama_base_url = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        self.ollama_model = os.environ.get("OLLAMA_MODEL", "llama3.2")
        setup_logging()

    def get_llm(self, temperature=0.7):
        """Get language model based on configuration"""
        if self.llm_provider == "ollama":
            return ChatOllama(
                model=self.ollama_model,
                base_url=self.ollama_base_url,
                temperature=temperature
            )
        else:
            raise ValueError(f"Unknown LLM provider: {self.llm_provider}")

# TODO: move this to a separate file
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )