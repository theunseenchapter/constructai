#!/usr/bin/env python3
import requests
import json

# Test the API endpoint
config = {
    'scene_type': 'architectural_visualization',
    'quality': 'professional',
    'rooms': [
        {
            'name': 'test_living_room',
            'type': 'living_room',
            'width': 22,
            'length': 18,
            'height': 3,
            'position': {'x': 0, 'y': 0, 'z': 0}
        }
    ],
    'building_dimensions': {
        'total_width': 22,
        'total_length': 18,
        'height': 3
    }
}

# Wrap config in the correct API format
api_request = {
    'tool': 'generate_3d_model',
    'arguments': config
}

try:
    print("🚀 Testing API endpoint...")
    response = requests.post('http://localhost:3000/api/mcp/blender-bridge', json=api_request, timeout=120)
    print('Status:', response.status_code)
    data = response.json()
    print('Full response:', json.dumps(data, indent=2))
    
    if response.status_code == 200:
        scene_id = data.get('result', {}).get('scene_id')
        files = data.get('result', {}).get('file_paths', {})
        print('Scene ID:', scene_id)
        print('Files:', len([f for f in files.values() if f]))
        for file_type, file_url in files.items():
            if file_url:
                print(f'  - {file_type}: {file_url}')
        for file in data.get('files', []):
            print(f'  - {file.get("name", "unknown")} ({file.get("size", 0)} bytes)')
            print(f'    URL: {file.get("url", "no url")}')
    else:
        print('Error:', response.text)
except Exception as e:
    print('Exception:', e)
