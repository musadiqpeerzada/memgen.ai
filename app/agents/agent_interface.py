# create an agent interface that all agents will implement
from abc import ABC


class AgentInterface(ABC):
    def __init__(self, config):
        self.config = config
        self.llm = config.get_llm()
    
    def do(self, *args, **kwargs):
        """Main method to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement this method.")
