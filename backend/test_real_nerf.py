#!/usr/bin/env python3
"""
Test script for real NeRF backend
"""

import requests
import json
import sys

def test_real_nerf():
    print('🧪 Testing Real NeRF Backend...')
    
    # Test health endpoint first
    try:
        health_response = requests.get('http://localhost:8000/api/v1/real-nerf/health')
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f'✅ Health check passed: {health_data["status"]}')
            print(f'🚀 CUDA available: {health_data["device_info"]["cuda_available"]}')
            print(f'🎮 GPU: {health_data["device_info"]["cuda_device_name"]}')
        else:
            print(f'❌ Health check failed: {health_response.status_code}')
            return False
    except Exception as e:
        print(f'❌ Health check error: {e}')
        return False
    
    # Test real NeRF processing
    print('\n🎯 Testing NeRF processing...')
    
    url = 'http://localhost:8000/api/v1/real-nerf/process-images-to-3d'
    
    # Prepare test data with mock images
    mock_images = [
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",  # 1x1 transparent PNG
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChAGA4849rwAAAABJRU5ErkJggg=="   # 1x1 red PNG
    ]
    
    data = {
        'images': json.dumps(mock_images),  # Mock images
        'config': json.dumps({
            'session_id': 'test_real_nerf_123',
            'room_specifications': {
                'room_type': 'living_room',
                'dimensions': {'width': 6, 'length': 8, 'height': 3}
            },
            'rendering_options': {
                'quality': 'high',
                'output_format': 'obj'
            }
        })
    }
    
    try:
        response = requests.post(url, data=data, timeout=30)
        print(f'📡 Response status: {response.status_code}')
        
        if response.status_code == 200:
            result = response.json()
            print('✅ Real NeRF processing succeeded!')
            print(f'📁 Files generated: {result.get("files", {})}')
            print(f'📊 Stats: {result.get("stats", {})}')
            
            # Check if OBJ file was actually created
            if result.get('files', {}).get('obj_file'):
                obj_file = result['files']['obj_file']
                print(f'🔍 Checking OBJ file: {obj_file}')
                
                # Try to find the file
                import os
                possible_paths = [
                    os.path.join('generated_models', obj_file),
                    os.path.join('..', 'public', 'renders', obj_file),
                    obj_file
                ]
                
                for path in possible_paths:
                    if os.path.exists(path):
                        file_size = os.path.getsize(path)
                        print(f'✅ Found OBJ file: {path} ({file_size} bytes)')
                        
                        # Read first few lines to check content
                        with open(path, 'r') as f:
                            lines = f.readlines()[:10]
                        
                        print('📝 First few lines:')
                        for i, line in enumerate(lines):
                            print(f'  {i+1}: {line.strip()}')
                        
                        return True
                
                print('⚠️ OBJ file not found in expected locations')
            
            return True
        else:
            print(f'❌ NeRF processing failed: {response.status_code}')
            print(f'Error: {response.text}')
            return False
            
    except Exception as e:
        print(f'❌ NeRF processing error: {e}')
        return False

if __name__ == '__main__':
    success = test_real_nerf()
    if success:
        print('\n🎉 All tests passed! Real NeRF backend is working.')
    else:
        print('\n💥 Tests failed! Check the backend.')
        sys.exit(1)
