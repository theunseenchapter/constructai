# ConstructAI API Gateway
# FastAPI-based microservices gateway with authentication and routing

from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
import httpx
import asyncio
import time
import logging
from typing import Optional, Dict, Any
import os
from contextlib import asynccontextmanager

# Configuration
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:password@localhost:5432/constructai")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    
    # Service URLs
    USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8000")
    PROJECT_SERVICE_URL = os.getenv("PROJECT_SERVICE_URL", "http://project-service:8000")
    FILE_SERVICE_URL = os.getenv("FILE_SERVICE_URL", "http://file-service:8000")
    BOQ_SERVICE_URL = os.getenv("BOQ_SERVICE_URL", "http://boq-service:8000")
    CHATBOT_SERVICE_URL = os.getenv("CHATBOT_SERVICE_URL", "http://chatbot-service:8000")
    VISION_SERVICE_URL = os.getenv("VISION_SERVICE_URL", "http://vision-service:8080")
    CONVERSION_SERVICE_URL = os.getenv("CONVERSION_SERVICE_URL", "http://conversion-service:8080")

config = Config()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# HTTP client for service communication
http_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global http_client
    http_client = httpx.AsyncClient(timeout=30.0)
    logger.info("API Gateway started")
    yield
    # Shutdown
    await http_client.aclose()
    logger.info("API Gateway shutdown")

# Create FastAPI app
app = FastAPI(
    title="ConstructAI API Gateway",
    description="Central API Gateway for ConstructAI microservices",
    version="1.0.0",
    lifespan=lifespan
)

# Security
security = HTTPBearer()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:19006"],  # Next.js and Expo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.constructai.com"]
)

# Service health check endpoints
SERVICE_HEALTH_URLS = {
    "user": f"{config.USER_SERVICE_URL}/health",
    "project": f"{config.PROJECT_SERVICE_URL}/health",
    "file": f"{config.FILE_SERVICE_URL}/health",
    "boq": f"{config.BOQ_SERVICE_URL}/health",
    "chatbot": f"{config.CHATBOT_SERVICE_URL}/health",
    "vision": f"{config.VISION_SERVICE_URL}/health",
    "conversion": f"{config.CONVERSION_SERVICE_URL}/health",
}

# Route mapping
SERVICE_ROUTES = {
    "/auth": config.USER_SERVICE_URL,
    "/users": config.USER_SERVICE_URL,
    "/projects": config.PROJECT_SERVICE_URL,
    "/files": config.FILE_SERVICE_URL,
    "/boq": config.BOQ_SERVICE_URL,
    "/chat": config.CHATBOT_SERVICE_URL,
    "/vision": config.VISION_SERVICE_URL,
    "/3d": config.CONVERSION_SERVICE_URL,
}

# Middleware for request logging and metrics
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log response
    logger.info(f"Response: {response.status_code} - {process_time:.4f}s")
    
    return response

# Authentication middleware
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Optional[Dict[str, Any]]:
    """Verify JWT token with user service"""
    try:
        response = await http_client.post(
            f"{config.USER_SERVICE_URL}/auth/verify",
            headers={"Authorization": f"Bearer {credentials.credentials}"}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=401, detail="Invalid token")
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Authentication service unavailable")

# Optional authentication for public endpoints
async def optional_auth(request: Request) -> Optional[Dict[str, Any]]:
    """Optional authentication for endpoints that can work with or without auth"""
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        try:
            credentials = HTTPAuthorizationCredentials(
                scheme="Bearer",
                credentials=auth_header.split(" ")[1]
            )
            return await verify_token(credentials)
        except HTTPException:
            return None
    return None

# Health check endpoint
@app.get("/health")
async def health_check():
    """Gateway health check"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "services": await check_service_health()
    }

async def check_service_health():
    """Check health of all microservices"""
    health_status = {}
    
    for service_name, health_url in SERVICE_HEALTH_URLS.items():
        try:
            response = await http_client.get(health_url, timeout=5.0)
            health_status[service_name] = {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "response_time": response.elapsed.total_seconds()
            }
        except httpx.RequestError:
            health_status[service_name] = {
                "status": "unreachable",
                "response_time": None
            }
    
    return health_status

# Service proxy function
async def proxy_request(
    request: Request,
    target_url: str,
    user_info: Optional[Dict[str, Any]] = None
) -> Response:
    """Proxy request to target microservice"""
    
    # Prepare headers
    headers = dict(request.headers)
    
    # Add user context if authenticated
    if user_info:
        headers["X-User-ID"] = user_info.get("user_id", "")
        headers["X-User-Role"] = user_info.get("role", "")
    
    # Remove host header to avoid conflicts
    headers.pop("host", None)
    
    try:
        # Get request body for POST/PUT requests
        body = None
        if request.method in ["POST", "PUT", "PATCH"]:
            body = await request.body()
        
        # Make request to target service
        response = await http_client.request(
            method=request.method,
            url=f"{target_url}{request.url.path}",
            params=request.query_params,
            headers=headers,
            content=body
        )
        
        # Return response
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.headers.get("content-type")
        )
        
    except httpx.RequestError as e:
        logger.error(f"Service request failed: {e}")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")

# Authentication routes (no auth required)
@app.api_route("/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def auth_proxy(request: Request, path: str):
    """Proxy authentication requests"""
    return await proxy_request(request, config.USER_SERVICE_URL)

# Protected routes with authentication
@app.api_route("/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def users_proxy(request: Request, path: str, user_info: dict = Depends(verify_token)):
    """Proxy user management requests"""
    return await proxy_request(request, config.USER_SERVICE_URL, user_info)

@app.api_route("/projects/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def projects_proxy(request: Request, path: str, user_info: dict = Depends(verify_token)):
    """Proxy project management requests"""
    return await proxy_request(request, config.PROJECT_SERVICE_URL, user_info)

@app.api_route("/files/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def files_proxy(request: Request, path: str, user_info: dict = Depends(verify_token)):
    """Proxy file management requests"""
    return await proxy_request(request, config.FILE_SERVICE_URL, user_info)

@app.api_route("/boq/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def boq_proxy(request: Request, path: str, user_info: dict = Depends(verify_token)):
    """Proxy BOQ management requests"""
    return await proxy_request(request, config.BOQ_SERVICE_URL, user_info)

@app.api_route("/chat/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def chat_proxy(request: Request, path: str, user_info: dict = Depends(verify_token)):
    """Proxy chatbot requests"""
    return await proxy_request(request, config.CHATBOT_SERVICE_URL, user_info)

# AI service routes (with optional auth for some endpoints)
@app.api_route("/vision/{path:path}", methods=["GET", "POST"])
async def vision_proxy(request: Request, path: str, user_info: dict = Depends(verify_token)):
    """Proxy computer vision requests"""
    return await proxy_request(request, config.VISION_SERVICE_URL, user_info)

@app.api_route("/3d/{path:path}", methods=["GET", "POST"])
async def conversion_proxy(request: Request, path: str, user_info: dict = Depends(verify_token)):
    """Proxy 3D conversion requests"""
    return await proxy_request(request, config.CONVERSION_SERVICE_URL, user_info)

# WebSocket support for real-time features
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
    
    def disconnect(self, user_id: str):
        self.active_connections.pop(user_id, None)
    
    async def send_personal_message(self, message: str, user_id: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle real-time messages (notifications, chat, etc.)
            await manager.send_personal_message(f"Echo: {data}", user_id)
    except WebSocketDisconnect:
        manager.disconnect(user_id)

# API documentation
@app.get("/")
async def root():
    """API Gateway information"""
    return {
        "name": "ConstructAI API Gateway",
        "version": "1.0.0",
        "environment": config.ENVIRONMENT,
        "docs": "/docs",
        "health": "/health"
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "status_code": 500
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=config.ENVIRONMENT == "development",
        log_level="info"
    )
