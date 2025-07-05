from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# Base schemas
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

# Project schemas
class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    budget: Optional[float] = None
    location: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    budget: Optional[float] = None
    location: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class Project(ProjectBase):
    id: int
    status: str
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

# File schemas
class FileBase(BaseModel):
    filename: str
    original_filename: str
    file_type: str
    category: str

class FileUpload(BaseModel):
    category: str = Field(..., description="File category: blueprint, photo, document, 3d_model")
    project_id: Optional[int] = None

class File(FileBase):
    id: int
    file_size: int
    file_path: str
    project_id: Optional[int] = None
    uploaded_by_id: int
    processing_status: str
    processing_result: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

# BOQ schemas
class BOQItemBase(BaseModel):
    item_code: str
    description: str
    unit: str
    quantity: float = Field(..., gt=0)
    rate: float = Field(..., gt=0)
    category: str
    subcategory: Optional[str] = None

class BOQItemCreate(BOQItemBase):
    project_id: int

class BOQItemUpdate(BaseModel):
    description: Optional[str] = None
    unit: Optional[str] = None
    quantity: Optional[float] = None
    rate: Optional[float] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None

class BOQItem(BOQItemBase):
    id: int
    project_id: int
    amount: float
    extracted_from_blueprint: bool
    confidence_score: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

# Safety Report schemas
class SafetyReportBase(BaseModel):
    report_type: str
    severity: str = Field(..., regex="^(low|medium|high|critical)$")
    title: str
    description: Optional[str] = None
    recommendations: Optional[str] = None

class SafetyReportCreate(SafetyReportBase):
    project_id: int
    image_file_id: Optional[int] = None
    detection_confidence: Optional[float] = None
    detection_bbox: Optional[Dict[str, float]] = None

class SafetyReportUpdate(BaseModel):
    status: Optional[str] = None
    description: Optional[str] = None
    recommendations: Optional[str] = None

class SafetyReport(SafetyReportBase):
    id: int
    project_id: int
    status: str
    image_file_id: Optional[int] = None
    detection_confidence: Optional[float] = None
    detection_bbox: Optional[Dict[str, float]] = None
    detected_at: datetime
    resolved_at: Optional[datetime] = None

# Chat schemas
class ChatSessionCreate(BaseModel):
    project_id: Optional[int] = None
    session_title: Optional[str] = None
    language: str = "en"

class ChatSession(BaseModel):
    id: int
    user_id: int
    project_id: Optional[int] = None
    session_title: Optional[str] = None
    language: str
    created_at: datetime

class ChatMessageCreate(BaseModel):
    content: str
    content_type: str = "text"

class ChatMessage(BaseModel):
    id: int
    session_id: int
    role: str
    content: str
    content_type: str
    tokens_used: Optional[int] = None
    processing_time: Optional[float] = None
    created_at: datetime

# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginData(BaseModel):
    username: str
    password: str

# API Response schemas
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int

# AI Processing schemas
class BlueprintProcessingResult(BaseModel):
    detected_elements: List[Dict[str, Any]]
    estimated_quantities: Dict[str, float]
    confidence_scores: Dict[str, float]
    processing_time: float

class VisionAnalysisResult(BaseModel):
    detections: List[Dict[str, Any]]
    safety_violations: List[Dict[str, Any]]
    confidence_scores: List[float]
    recommendations: List[str]
