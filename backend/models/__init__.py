from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from ..core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    projects = relationship("Project", back_populates="owner")
    files = relationship("File", back_populates="uploaded_by")

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="active")  # active, completed, archived
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Project metadata
    budget = Column(Float, nullable=True)
    location = Column(String(255), nullable=True)
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    owner = relationship("User", back_populates="projects")
    files = relationship("File", back_populates="project")
    boq_items = relationship("BOQItem", back_populates="project")
    safety_reports = relationship("SafetyReport", back_populates="project")

class File(Base):
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)  # MinIO path
    file_type = Column(String(100), nullable=False)  # MIME type
    file_size = Column(Integer, nullable=False)  # bytes
    
    # File categorization
    category = Column(String(50), nullable=False)  # blueprint, photo, document, 3d_model
    
    # Relationships
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    uploaded_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    project = relationship("Project", back_populates="files")
    uploaded_by = relationship("User", back_populates="files")
    
    # Processing status
    processing_status = Column(String(50), default="pending")  # pending, processing, completed, failed
    processing_result = Column(JSON, nullable=True)  # Store AI processing results
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class BOQItem(Base):
    __tablename__ = "boq_items"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    # Item details
    item_code = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    unit = Column(String(20), nullable=False)  # sqm, cum, nos, etc.
    quantity = Column(Float, nullable=False)
    rate = Column(Float, nullable=False)  # per unit cost
    amount = Column(Float, nullable=False)  # quantity * rate
    
    # Categories
    category = Column(String(100), nullable=False)  # earthwork, concrete, steel, etc.
    subcategory = Column(String(100), nullable=True)
    
    # AI Analysis
    extracted_from_blueprint = Column(Boolean, default=False)
    confidence_score = Column(Float, nullable=True)  # AI confidence 0-1
    
    project = relationship("Project", back_populates="boq_items")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class SafetyReport(Base):
    __tablename__ = "safety_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    # Report details
    report_type = Column(String(50), nullable=False)  # ppe_violation, crack_detection, progress_tracking
    severity = Column(String(20), nullable=False)  # low, medium, high, critical
    status = Column(String(20), default="open")  # open, in_progress, resolved
    
    # Detection details
    image_file_id = Column(Integer, ForeignKey("files.id"), nullable=True)
    detection_confidence = Column(Float, nullable=True)
    detection_bbox = Column(JSON, nullable=True)  # Bounding box coordinates
    
    # Description
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    recommendations = Column(Text, nullable=True)
    
    # Timestamps
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    
    project = relationship("Project", back_populates="safety_reports")
    image_file = relationship("File")

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    
    session_title = Column(String(255), nullable=True)
    language = Column(String(10), default="en")  # en, hi, te, ta, etc.
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    project = relationship("Project")
    messages = relationship("ChatMessage", back_populates="session")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    
    # Message content
    role = Column(String(20), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    content_type = Column(String(20), default="text")  # text, image, audio
    
    # Metadata
    tokens_used = Column(Integer, nullable=True)
    processing_time = Column(Float, nullable=True)  # seconds
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    session = relationship("ChatSession", back_populates="messages")
