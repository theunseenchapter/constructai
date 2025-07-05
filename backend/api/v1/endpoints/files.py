from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List, Optional
from pydantic import BaseModel
import uuid
from datetime import datetime

router = APIRouter()

# Simplified models
class FileInfo(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_size: int
    content_type: str
    upload_date: datetime
    project_id: Optional[int] = None

class APIResponse(BaseModel):
    message: str
    data: Optional[dict] = None

# Mock data
mock_files = []

@router.post("/upload", response_model=APIResponse, summary="Upload file")
async def upload_file(
    file: UploadFile = File(...),
    project_id: Optional[int] = Form(None)
):
    """Upload a file (blueprints, images, documents)"""
    
    # Read file content
    file_content = await file.read()
    
    # Basic validation
    allowed_types = ["image/jpeg", "image/png", "image/webp", "application/pdf", "text/plain"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file.content_type} not allowed. Allowed types: {allowed_types}"
        )
    
    max_size = 100 * 1024 * 1024  # 100MB
    if len(file_content) > max_size:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {max_size} bytes"
        )
    
    # Generate unique filename
    file_extension = file.filename.split('.')[-1] if '.' in file.filename else ''
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    
    # Mock file storage (in production, save to MinIO/S3)
    file_info = FileInfo(
        id=len(mock_files) + 1,
        filename=unique_filename,
        original_filename=file.filename,
        file_size=len(file_content),
        content_type=file.content_type,
        upload_date=datetime.now(),
        project_id=project_id
    )
    
    mock_files.append(file_info)
    
    return APIResponse(
        message="File uploaded successfully",
        data={
            "file_id": file_info.id,
            "filename": file_info.filename,
            "size": file_info.file_size,
            "url": f"/api/v1/files/{file_info.id}/download"
        }
    )

@router.get("/", response_model=List[FileInfo], summary="List all files")
async def list_files(project_id: Optional[int] = None):
    """List all uploaded files"""
    if project_id:
        return [f for f in mock_files if f.project_id == project_id]
    return mock_files

@router.get("/{file_id}", response_model=FileInfo, summary="Get file info")
async def get_file(file_id: int):
    """Get file information by ID"""
    file_info = next((f for f in mock_files if f.id == file_id), None)
    if not file_info:
        raise HTTPException(status_code=404, detail="File not found")
    return file_info

@router.get("/{file_id}/download", summary="Download file")
async def download_file(file_id: int):
    """Download a file by ID"""
    file_info = next((f for f in mock_files if f.id == file_id), None)
    if not file_info:
        raise HTTPException(status_code=404, detail="File not found")
    
    # In production, return actual file content from MinIO/S3
    return APIResponse(
        message="File download URL generated",
        data={
            "download_url": f"https://storage.constructai.com/{file_info.filename}",
            "expires_in": "1 hour"
        }
    )

@router.delete("/{file_id}", response_model=APIResponse, summary="Delete file")
async def delete_file(file_id: int):
    """Delete a file by ID"""
    global mock_files
    file_info = next((f for f in mock_files if f.id == file_id), None)
    if not file_info:
        raise HTTPException(status_code=404, detail="File not found")
    
    mock_files = [f for f in mock_files if f.id != file_id]
    
    return APIResponse(
        message="File deleted successfully",
        data={"file_id": file_id}
    )
