from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# Simplified models for now
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    location: Optional[str] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None

class Project(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    location: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class APIResponse(BaseModel):
    message: str
    data: Optional[dict] = None

# Mock data for development
mock_projects = [
    Project(
        id=1,
        name="City Mall Construction",
        description="Multi-story shopping mall project",
        location="Downtown, City Center",
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    Project(
        id=2,
        name="Residential Complex",
        description="50-unit apartment complex",
        location="Suburb Area",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
]

@router.post("/", response_model=APIResponse, summary="Create new project")
async def create_project(project: ProjectCreate):
    """Create a new construction project"""
    new_project = Project(
        id=len(mock_projects) + 1,
        name=project.name,
        description=project.description,
        location=project.location,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    mock_projects.append(new_project)
    
    return APIResponse(
        message="Project created successfully",
        data=new_project.dict()
    )

@router.get("/", response_model=List[Project], summary="Get all projects")
async def get_projects(skip: int = 0, limit: int = 100):
    """Get all construction projects"""
    return mock_projects[skip : skip + limit]

@router.get("/{project_id}", response_model=Project, summary="Get project by ID")
async def get_project(project_id: int):
    """Get a specific project by ID"""
    project = next((p for p in mock_projects if p.id == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=APIResponse, summary="Update project")
async def update_project(project_id: int, project_update: ProjectUpdate):
    """Update project information"""
    project = next((p for p in mock_projects if p.id == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Update fields
    if project_update.name is not None:
        project.name = project_update.name
    if project_update.description is not None:
        project.description = project_update.description
    if project_update.location is not None:
        project.location = project_update.location
    
    project.updated_at = datetime.now()
    
    return APIResponse(
        message="Project updated successfully",
        data=project.dict()
    )

@router.delete("/{project_id}", response_model=APIResponse, summary="Delete project")
async def delete_project(project_id: int):
    """Delete a project"""
    global mock_projects
    project = next((p for p in mock_projects if p.id == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    mock_projects = [p for p in mock_projects if p.id != project_id]
    
    return APIResponse(
        message="Project deleted successfully",
        data={"project_id": project_id}
    )
