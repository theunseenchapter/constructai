from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
async def test_endpoint():
    """Test endpoint to verify API is working"""
    return {
        "message": "API is working!",
        "status": "success",
        "timestamp": "2025-01-01T00:00:00Z"
    }

@router.get("/")
async def api_root():
    """API v1 root endpoint"""
    return {
        "message": "ConstructAI API v1",
        "version": "1.0.0",
        "endpoints": [
            "/auth",
            "/users", 
            "/projects",
            "/files",
            "/boq",
            "/safety",
            "/chat",
            "/ai"
        ]
    }
