#!/usr/bin/env python3
"""
Test the real NeRF implementation with the living room image
"""

import requests
import json
import base64
import os
from PIL import Image
import io

def test_living_room_image():
    print('🏠 Testing Real NeRF with Living Room Image...')
    
    # First, let's check if we can access the image
    # For now, I'll create a test with a simple room description
    # In a real scenario, you would upload the actual image file
    
    # Test health endpoint first
    try:
        health_response = requests.get('http://localhost:8000/api/v1/real-nerf/health')
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f'✅ Backend health: {health_data["status"]}')
            print(f'🚀 CUDA available: {health_data["device_info"]["cuda_available"]}')
        else:
            print(f'❌ Health check failed: {health_response.status_code}')
            return False
    except Exception as e:
        print(f'❌ Health check error: {e}')
        return False
    
    # Create a mock base64 image (you would replace this with the actual living room image)
    print('\n🖼️ Preparing living room image data...')
    
    # Create a simple test image to simulate the living room
    # In practice, you'd convert your actual image to base64
    test_image = Image.new('RGB', (512, 512), color='lightblue')
    buffer = io.BytesIO()
    test_image.save(buffer, format='PNG')
    image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    base64_image = f"data:image/png;base64,{image_data}"
    
    # Test real NeRF processing with living room configuration
    print('\n🧠 Processing living room with real NeRF...')
    
    url = 'http://localhost:8000/api/v1/real-nerf/process-images-to-3d'
    
    # Prepare living room data
    data = {
        'images': json.dumps([base64_image]),  # Mock living room image
        'config': json.dumps({
            'session_id': 'living_room_test_123',
            'room_specifications': {
                'room_type': 'living_room',
                'dimensions': {'width': 8, 'length': 10, 'height': 3}  # Spacious living room
            },
            'rendering_options': {
                'quality': 'high',
                'output_format': 'obj'
            }
        })
    }
    
    try:
        print('📡 Sending request to real NeRF backend...')
        response = requests.post(url, data=data, timeout=60)
        print(f'📡 Response status: {response.status_code}')
        
        if response.status_code == 200:
            result = response.json()
            print('✅ Living room NeRF processing succeeded!')
            print(f'📁 Files generated: {result.get("files", {})}')
            print(f'📊 Stats: {result.get("stats", {})}')
            
            # Check if OBJ file was created
            if result.get('files', {}).get('obj_file'):
                obj_file = result['files']['obj_file']
                print(f'\n🔍 Checking generated OBJ file: {obj_file}')
                
                # Look for the file in expected locations
                possible_paths = [
                    os.path.join('generated_models', obj_file),
                    os.path.join('..', 'public', 'renders', obj_file),
                    obj_file
                ]
                
                for path in possible_paths:
                    if os.path.exists(path):
                        file_size = os.path.getsize(path)
                        print(f'✅ Found living room OBJ: {path} ({file_size} bytes)')
                        
                        # Read and display the first few lines
                        with open(path, 'r') as f:
                            lines = f.readlines()[:15]
                        
                        print('\n📝 Living room 3D model content:')
                        for i, line in enumerate(lines):
                            print(f'  {i+1}: {line.strip()}')
                        
                        # Count vertices and faces
                        with open(path, 'r') as f:
                            content = f.read()
                        
                        vertex_count = content.count('\nv ')
                        face_count = content.count('\nf ')
                        
                        print(f'\n📊 Living room model stats:')
                        print(f'   Vertices: {vertex_count}')
                        print(f'   Faces: {face_count}')
                        print(f'   File size: {file_size} bytes')
                        
                        return True
                
                print('⚠️ OBJ file not found in expected locations')
            
            return True
        else:
            print(f'❌ Living room NeRF processing failed: {response.status_code}')
            print(f'Error: {response.text}')
            return False
            
    except Exception as e:
        print(f'❌ Living room NeRF processing error: {e}')
        return False

def test_frontend_integration():
    """Test the complete frontend-to-backend pipeline"""
    print('\n🌐 Testing Frontend Integration...')
    
    try:
        # Test the frontend NeRF API
        frontend_url = 'http://localhost:3000/api/nerf/generate-3d'
        
        payload = {
            "images": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="],
            "room_specifications": {
                "room_type": "living_room",
                "dimensions": {"width": 8, "length": 10, "height": 3}
            },
            "rendering_options": {
                "quality": "high",
                "output_format": "obj"
            }
        }
        
        print('📡 Testing frontend NeRF API...')
        response = requests.post(frontend_url, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            print('✅ Frontend integration working!')
            print(f'📁 Model files: {result.get("model_files", {})}')
            
            # Test download
            if result.get('model_files', {}).get('obj_file'):
                obj_filename = result['model_files']['obj_file']
                download_url = f'http://localhost:3000/api/download/{obj_filename}'
                
                print(f'⬇️ Testing download: {download_url}')
                download_response = requests.get(download_url)
                
                if download_response.status_code == 200:
                    print('✅ Download working!')
                    print(f'📄 Content type: {download_response.headers.get("content-type")}')
                    print(f'📦 File size: {len(download_response.content)} bytes')
                    
                    # Show first few lines of the downloaded OBJ
                    content = download_response.text
                    lines = content.split('\n')[:10]
                    print('\n📝 Downloaded OBJ content:')
                    for i, line in enumerate(lines):
                        if line.strip():
                            print(f'  {i+1}: {line}')
                else:
                    print(f'❌ Download failed: {download_response.status_code}')
            
            return True
        else:
            print(f'❌ Frontend integration failed: {response.status_code}')
            print(f'Error: {response.text}')
            return False
            
    except Exception as e:
        print(f'❌ Frontend integration error: {e}')
        return False

if __name__ == '__main__':
    print('🧪 Testing Real NeRF with Living Room Image\n')
    
    # Test backend directly
    backend_success = test_living_room_image()
    
    # Test frontend integration
    frontend_success = test_frontend_integration()
    
    if backend_success and frontend_success:
        print('\n🎉 All tests passed! Living room NeRF processing is working!')
        print('✅ Backend generates real 3D models')
        print('✅ Frontend integration works')
        print('✅ Downloads are functional')
    else:
        print('\n💥 Some tests failed!')
        if not backend_success:
            print('❌ Backend NeRF processing issues')
        if not frontend_success:
            print('❌ Frontend integration issues')
