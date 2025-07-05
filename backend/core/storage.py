# Optional storage imports
try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None

try:
    from minio import Minio
    MINIO_AVAILABLE = True
except ImportError:
    MINIO_AVAILABLE = False
    Minio = None

from core.config import settings

# Redis client
if REDIS_AVAILABLE:
    redis_client = redis.from_url(settings.redis_url)
else:
    redis_client = None

# MinIO client
if MINIO_AVAILABLE:
    minio_client = Minio(
        settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=settings.minio_secure
    )
else:
    minio_client = None

# Initialize MinIO bucket
def init_minio():
    """Initialize MinIO bucket if it doesn't exist"""
    if not MINIO_AVAILABLE or minio_client is None:
        print("⚠️ MinIO not available, skipping bucket initialization")
        return
        
    try:
        if not minio_client.bucket_exists(settings.minio_bucket):
            minio_client.make_bucket(settings.minio_bucket)
            print(f"Created bucket: {settings.minio_bucket}")
        else:
            print(f"Bucket {settings.minio_bucket} already exists")
    except Exception as e:
        print(f"Error initializing MinIO: {e}")

# Storage helper functions
async def upload_file(file_data: bytes, filename: str, content_type: str) -> str:
    """Upload file to MinIO and return the file path"""
    if not MINIO_AVAILABLE or minio_client is None:
        print("⚠️ MinIO not available, skipping file upload")
        return f"local://{filename}"
        
    try:
        minio_client.put_object(
            settings.minio_bucket,
            filename,
            io.BytesIO(file_data),
            len(file_data),
            content_type=content_type
        )
        return f"minio://{settings.minio_bucket}/{filename}"
    except Exception as e:
        raise Exception(f"Failed to upload file: {e}")

async def get_file_url(filename: str) -> str:
    """Get presigned URL for file"""
    try:
        return minio_client.presigned_get_object(
            settings.minio_bucket,
            filename,
            expires=3600  # 1 hour
        )
    except Exception as e:
        raise Exception(f"Failed to get file URL: {e}")

import io
