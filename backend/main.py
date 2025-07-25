from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager

from core.config import settings
from api.v1 import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("🚀 Starting ConstructAI Backend...")
    
    # Initialize CUDA optimizations
    try:
        from cuda_performance_optimizer import cuda_optimizer
        cuda_optimizer.apply_cuda_optimizations()
        print("⚡ CUDA 12.1 optimizations applied successfully!")
    except ImportError:
        print("⚠️ CUDA optimizations not available - using CPU mode")
    
    # Skip database initialization for now (development mode)
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    print("⚠️ Database initialization skipped (development mode)")

    # Skip MinIO initialization for now (development mode)
    # init_minio()
    print("⚠️ MinIO initialization skipped (development mode)")

    print("🎉 ConstructAI Backend is ready!")

    yield

    # Shutdown
    print("👋 Shutting down ConstructAI Backend...")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="AI-Powered Construction Management Backend",
    version=settings.version,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan
)

# Security
security = HTTPBearer()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure for production
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "constructai-backend",
        "version": settings.version,
        "timestamp": "2025-01-01T00:00:00Z"
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🏗️ ConstructAI Backend API",
        "version": settings.version,
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting ConstructAI Backend server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
