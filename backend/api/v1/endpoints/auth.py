from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

router = APIRouter()
security = HTTPBearer()

# Simple Pydantic models for auth
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None

class LoginData(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool = True

class APIResponse(BaseModel):
    message: str
    data: Optional[dict] = None

@router.post("/register", response_model=APIResponse, summary="Register new user")
async def register_user(user_data: UserCreate):
    """Register a new user account"""
    # Mock implementation for now
    return APIResponse(
        message="User registered successfully",
        data={
            "user_id": 1,
            "username": user_data.username,
            "email": user_data.email
        }
    )

@router.post("/login", response_model=Token, summary="User login")
async def login_user(login_data: LoginData):
    """Authenticate user and return access token"""
    # Mock implementation for now
    if login_data.username == "admin" and login_data.password == "password":
        return Token(
            access_token="mock_jwt_token_12345",
            token_type="bearer"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/me", response_model=User, summary="Get current user")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user information"""
    # Mock implementation for now
    token = credentials.credentials
    if token == "mock_jwt_token_12345":
        return User(
            id=1,
            username="admin",
            email="admin@constructai.com",
            full_name="ConstructAI Admin",
            is_active=True
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/logout", response_model=APIResponse, summary="User logout")
async def logout_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Logout user (invalidate token)"""
    return APIResponse(message="User logged out successfully")

@router.post("/refresh", response_model=Token, summary="Refresh access token")
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Refresh access token"""
    # Mock implementation for now
    return Token(
        access_token="mock_jwt_token_67890",
        token_type="bearer"
    )
