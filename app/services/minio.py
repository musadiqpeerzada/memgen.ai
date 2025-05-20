from urllib.parse import urlparse
from minio import Minio
from app.config import Config

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, config: Config, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(config, *args, **kwargs)
        return cls._instances[cls]

class MinioClient(metaclass=SingletonMeta):
    def __init__(self, config: Config):
        # Parse the minio base URL to extract the endpoint without scheme
        parsed_url = urlparse(config.minio_base_url)
        endpoint = parsed_url.netloc or parsed_url.path
        secure = parsed_url.scheme == "https"

        self.client = Minio(
            endpoint,
            access_key=config.minio_access_key,
            secret_key=config.minio_secret_key,
            secure=secure
        )
        self.bucket = config.minio_bucket
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)

    def put_file(self, file_stream, object_name: str, content_type="image/png"):
        self.client.put_object(
            self.bucket,
            object_name,
            file_stream,
            file_stream.getbuffer().nbytes,
            content_type=content_type
        )
        return self.client.get_presigned_url(self.bucket, object_name)
    
    def get_file_url(self, object_name: str):
        return self.client.presigned_get_object(self.bucket, object_name)
    
    def download_file(self, object_name: str, file_path: str):
        self.client.fget_object(self.bucket, object_name, file_path)

    def delete_file(self, object_name: str):
        self.client.remove_object(self.bucket, object_name)

    def list_files(self):
        objects = self.client.list_objects(self.bucket)
        return [obj.object_name for obj in objects]
    
    def file_exists(self, object_name: str):
        try:
            self.client.stat_object(self.bucket, object_name)
            return True
        except Exception:
            return False
    