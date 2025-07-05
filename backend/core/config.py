import os
from pydantic_settings import BaseSettings
from typing import Optional, List
from pydantic import field_validator


class Settings(BaseSettings):
    # App Config
    app_name: str = "ConstructAI Backend"
    debug: bool = True
    version: str = "1.0.0"
    
    # Database
    database_url: str = "postgresql+asyncpg://admin:password@localhost:5432/constructai"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # MinIO/S3
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin123"
    minio_bucket: str = "constructai-files"
    minio_secure: bool = False
    
    # JWT
    secret_key: str = "your-super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # AI Models
    ai_models_path: str = "./models"
    huggingface_cache_dir: str = "./cache/huggingface"
    torch_device: str = "cuda"
    
    # External APIs
    openai_api_key: Optional[str] = None
    
    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:3001,http://localhost:3002,http://localhost:3003,http://localhost:8080"
    
    @field_validator('cors_origins')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    # File Upload
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    allowed_file_types: str = "image/jpeg,image/png,image/webp,application/pdf,text/plain,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    
    @field_validator('allowed_file_types')
    @classmethod
    def parse_allowed_file_types(cls, v):
        if isinstance(v, str):
            return [file_type.strip() for file_type in v.split(',')]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields instead of raising error


settings = Settings()
