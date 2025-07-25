"""
Real NeRF API Endpoint for ConstructAI
Processes actual images and generates real 3D geometry
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
import json
import os
import tempfile
import shutil
from pathlib import Path
import logging
import traceback
import torch

# Import our real NeRF processor
from ai_models.real_nerf_processor import RealNeRFProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Global NeRF processor instance
nerf_processor = None

def get_nerf_processor():
    """Get or create NeRF processor instance"""
    global nerf_processor
    if nerf_processor is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        nerf_processor = RealNeRFProcessor(device)
        logger.info(f"🚀 Real NeRF processor initialized on {device}")
    return nerf_processor

@router.post("/process-images-to-3d")
async def process_images_to_3d(
    images: str = Form(...),  # JSON string of image data
    config: str = Form(...),  # JSON string of configuration
):
    """
    Process multiple images and generate real 3D model using NeRF
    
    Args:
        images: JSON string containing array of base64 image data
        config: JSON string containing NeRF configuration
    
    Returns:
        JSON response with generated 3D model information
    """
    try:
        logger.info("🎯 Starting real NeRF image-to-3D processing")
        
        # Parse inputs
        try:
            images_data = json.loads(images)
            config_data = json.loads(config)
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail=f"Invalid JSON input: {e}")
        
        # Validate inputs
        if not isinstance(images_data, list) or len(images_data) == 0:
            raise HTTPException(status_code=400, detail="At least one image is required")
        
        # Get NeRF processor
        processor = get_nerf_processor()
        
        # Set up output directory
        output_dir = os.path.join(os.getcwd(), "generated_models")
        os.makedirs(output_dir, exist_ok=True)
        
        # Also create public output directory for frontend access
        public_output_dir = os.path.join(os.getcwd(), "..", "public", "renders")
        os.makedirs(public_output_dir, exist_ok=True)
        
        # Process images to 3D
        result = processor.process_images_to_3d(
            images=images_data,
            config=config_data,
            output_dir=output_dir
        )
        
        if result.get('success'):
            # Copy files to public directory for frontend access
            if 'files' in result:
                public_files = {}
                for file_type, file_path in result['files'].items():
                    if os.path.exists(file_path):
                        filename = os.path.basename(file_path)
                        public_path = os.path.join(public_output_dir, filename)
                        shutil.copy2(file_path, public_path)
                        public_files[file_type] = filename  # Store just filename for frontend
                        logger.info(f"📁 Copied {file_type} to public directory: {filename}")
                
                result['files'] = public_files
            
            logger.info("✅ Real NeRF processing completed successfully")
            return JSONResponse(content=result)
        else:
            logger.error("❌ NeRF processing failed")
            raise HTTPException(status_code=500, detail="NeRF processing failed")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error in NeRF processing: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/upload-images-for-3d")
async def upload_images_for_3d(
    files: List[UploadFile] = File(...),
    room_type: str = Form("living_room"),
    quality: str = Form("high"),
    dimensions_width: float = Form(6.0),
    dimensions_length: float = Form(8.0),
    dimensions_height: float = Form(3.0),
):
    """
    Upload image files and process them for 3D reconstruction
    
    Args:
        files: List of uploaded image files
        room_type: Type of room being reconstructed
        quality: Quality level (draft, medium, high, ultra)
        dimensions_*: Room dimensions in meters
    
    Returns:
        JSON response with generated 3D model information
    """
    try:
        logger.info(f"🖼️ Processing {len(files)} uploaded files for 3D reconstruction")
        
        # Validate files
        if not files or len(files) == 0:
            raise HTTPException(status_code=400, detail="At least one image file is required")
        
        # Create temporary directory for uploaded files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded files
            image_paths = []
            for i, file in enumerate(files):
                if not file.content_type or not file.content_type.startswith('image/'):
                    logger.warning(f"Skipping non-image file: {file.filename}")
                    continue
                
                # Save file
                file_path = os.path.join(temp_dir, f"image_{i}_{file.filename}")
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                
                image_paths.append(file_path)
                logger.info(f"📥 Saved uploaded file: {file.filename}")
            
            if not image_paths:
                raise HTTPException(status_code=400, detail="No valid image files found")
            
            # Create configuration
            config = {
                'session_id': f'upload_{int(torch.rand(1).item() * 1000000)}',
                'room_specifications': {
                    'room_type': room_type,
                    'dimensions': {
                        'width': dimensions_width,
                        'length': dimensions_length,
                        'height': dimensions_height
                    }
                },
                'rendering_options': {
                    'quality': quality,
                    'output_format': 'obj'
                }
            }
            
            # Get NeRF processor
            processor = get_nerf_processor()
            
            # Set up output directory
            output_dir = os.path.join(os.getcwd(), "generated_models")
            os.makedirs(output_dir, exist_ok=True)
            
            # Also create public output directory
            public_output_dir = os.path.join(os.getcwd(), "..", "public", "renders")
            os.makedirs(public_output_dir, exist_ok=True)
            
            # Process images
            result = processor.process_images_to_3d(
                images=image_paths,  # Use file paths instead of base64
                config=config,
                output_dir=output_dir
            )
            
            if result.get('success'):
                # Copy files to public directory
                if 'files' in result:
                    public_files = {}
                    for file_type, file_path in result['files'].items():
                        if os.path.exists(file_path):
                            filename = os.path.basename(file_path)
                            public_path = os.path.join(public_output_dir, filename)
                            shutil.copy2(file_path, public_path)
                            public_files[file_type] = filename
                            logger.info(f"📁 Copied {file_type} to public directory: {filename}")
                    
                    result['files'] = public_files
                
                logger.info("✅ Upload and processing completed successfully")
                return JSONResponse(content=result)
            else:
                raise HTTPException(status_code=500, detail="Image processing failed")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Upload processing error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@router.get("/nerf-status/{session_id}")
async def get_nerf_status(session_id: str):
    """Get status of NeRF processing session"""
    try:
        # Check if session files exist
        output_dir = os.path.join(os.getcwd(), "generated_models")
        obj_file = os.path.join(output_dir, f"nerf_{session_id}.obj")
        ply_file = os.path.join(output_dir, f"nerf_{session_id}.ply")
        
        status = {
            'session_id': session_id,
            'status': 'completed' if os.path.exists(obj_file) else 'not_found',
            'files_available': {
                'obj': os.path.exists(obj_file),
                'ply': os.path.exists(ply_file)
            }
        }
        
        if status['status'] == 'completed':
            # Get file stats
            if os.path.exists(obj_file):
                file_size = os.path.getsize(obj_file)
                status['file_stats'] = {
                    'obj_size_bytes': file_size,
                    'obj_size_mb': round(file_size / (1024 * 1024), 2)
                }
        
        return JSONResponse(content=status)
    
    except Exception as e:
        logger.error(f"❌ Status check error: {e}")
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint for NeRF service"""
    try:
        device_info = {
            'cuda_available': torch.cuda.is_available(),
            'cuda_device_count': torch.cuda.device_count() if torch.cuda.is_available() else 0,
        }
        
        if torch.cuda.is_available():
            device_info.update({
                'cuda_device_name': torch.cuda.get_device_name(),
                'cuda_memory_total': torch.cuda.get_device_properties(0).total_memory,
                'cuda_memory_free': torch.cuda.get_device_properties(0).total_memory - torch.cuda.memory_allocated(),
            })
        
        return {
            'status': 'healthy',
            'service': 'real-nerf-processor',
            'device_info': device_info,
            'timestamp': torch.rand(1).item()  # Use torch for timestamp
        }
    
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={'status': 'unhealthy', 'error': str(e)}
        )

# Remove the problematic exception handler
# @router.exception_handler(Exception)
# async def global_exception_handler(request, exc):
#     logger.error(f"❌ Unhandled exception: {exc}")
#     logger.error(traceback.format_exc())
#     return JSONResponse(
#         status_code=500,
#         content={'error': 'Internal server error', 'detail': str(exc)}
#     )
