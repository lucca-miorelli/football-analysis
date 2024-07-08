from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class CentralConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # MinIO
    MINIO_ROOT_USER: Optional[str] = "admin"
    MINIO_ROOT_PASSWORD: Optional[str] = "Admin@123"
    MINIO_DEFAULT_BUCKET: Optional[str] = "football-analysis"

    # AWS
    AWS_BUCKET_NAME: str = "football-data-platform"
    AWS_ACCESS_KEY_ID: str = "admin"
    AWS_SECRET_ACCESS_KEY: str = "Admin@123"
    AWS_DEFAULT_REGION: str = "us-east-1"
    AWS_ENDPOINT_URL: Optional[str] = "http://localhost:9000"


cc: CentralConfig = CentralConfig()
