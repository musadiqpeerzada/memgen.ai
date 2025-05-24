from app.config import Config
from pinecone import Pinecone
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, config: Config, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(config, *args, **kwargs)
        return cls._instances[cls]

class PineconeClient(metaclass=SingletonMeta):
    def __init__(self, config: Config):
        self.api_key = config.pinecone_api_key
        self.index_name = config.pinecone_index_name
        self.client = Pinecone(
            api_key=self.api_key,
        )        

    def query(self, query_vector, top_k=1, include_metadata=True):
        index = self.client.Index(self.index_name)
        response = index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=include_metadata
        )
        return response
    
    def get_all(self):
        index = self.client.Index(self.index_name)
        response = index.fetch_all()
        return response