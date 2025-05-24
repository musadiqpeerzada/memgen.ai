# create an agent interface that all agents will implement
from abc import ABC
from app.config import Config
from app.models.llm_model import LLModel

class AgentInterface(ABC):
    def __init__(self, config: Config):
        self.config = config
        self.llm = LLModel.get_instance(config).llm
    
    def do(self, *args, **kwargs):
        """Main method to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement this method.")
