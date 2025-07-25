#!/usr/bin/env python3
"""
Quick test to verify the statistics are now working properly
"""

import requests
import json

def test_frontend_stats():
    print('🧪 Testing Frontend Stats Display...')
    
    # Test the frontend API
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
    
    try:
        print('📡 Testing frontend API...')
        response = requests.post(frontend_url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print('✅ Frontend API working!')
            
            # Check stats specifically
            if 'stats' in result:
                stats = result['stats']
                print(f'\n📊 Statistics received:')
                print(f'   Vertices: {stats.get("vertex_count", "N/A")}')
                print(f'   Faces: {stats.get("face_count", "N/A")}')
                print(f'   Processing Time: {stats.get("processing_time", "N/A")}s')
            else:
                print('❌ No stats field in response')
                print(f'Response keys: {list(result.keys())}')
            
            # Check model files
            if 'model_files' in result:
                model_files = result['model_files']
                print(f'\n📁 Model files:')
                for file_type, filename in model_files.items():
                    if filename:
                        print(f'   {file_type}: {filename}')
            
            return True
        else:
            print(f'❌ Frontend API failed: {response.status_code}')
            print(f'Error: {response.text}')
            return False
            
    except Exception as e:
        print(f'❌ Frontend API error: {e}')
        return False

if __name__ == '__main__':
    success = test_frontend_stats()
    if success:
        print('\n🎉 Stats test completed!')
    else:
        print('\n💥 Stats test failed!')
