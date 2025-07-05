#!/usr/bin/env python3
import requests
import json

def test_api_with_different_rooms():
    """Test the API with dramatically different room configurations"""
    
    # Test 1: Tiny bathroom
    tiny_config = {
        'tool': 'generate_3d_model',
        'arguments': {
            'scene_type': 'architectural_visualization',
            'quality': 'professional',
            'rooms': [
                {
                    'name': 'tiny_bathroom',
                    'type': 'bathroom',
                    'width': 5,
                    'length': 4,
                    'height': 2.5,
                    'position': {'x': 0, 'y': 0, 'z': 0}
                }
            ],
            'building_dimensions': {
                'total_width': 5,
                'total_length': 4,
                'height': 2.5
            }
        }
    }
    
    # Test 2: Massive living room
    huge_config = {
        'tool': 'generate_3d_model',
        'arguments': {
            'scene_type': 'architectural_visualization',
            'quality': 'professional',
            'rooms': [
                {
                    'name': 'mansion_living_room',
                    'type': 'living_room',
                    'width': 40,
                    'length': 30,
                    'height': 5,
                    'position': {'x': 0, 'y': 0, 'z': 0}
                }
            ],
            'building_dimensions': {
                'total_width': 40,
                'total_length': 30,
                'height': 5
            }
        }
    }
    
    print("🚽 TESTING TINY BATHROOM VIA API...")
    tiny_response = requests.post('http://localhost:3000/api/mcp/blender-bridge', json=tiny_config, timeout=120)
    if tiny_response.status_code == 200:
        tiny_data = tiny_response.json()
        print(f"✅ Tiny bathroom generated: {tiny_data.get('result', {}).get('scene_id')}")
        print(f"📁 Files: {len([f for f in tiny_data.get('result', {}).get('file_paths', {}).values() if f])}")
    else:
        print(f"❌ Tiny bathroom failed: {tiny_response.status_code}")
    
    print("\n🏰 TESTING MASSIVE LIVING ROOM VIA API...")
    huge_response = requests.post('http://localhost:3000/api/mcp/blender-bridge', json=huge_config, timeout=120)
    if huge_response.status_code == 200:
        huge_data = huge_response.json()
        print(f"✅ Huge living room generated: {huge_data.get('result', {}).get('scene_id')}")
        print(f"📁 Files: {len([f for f in huge_data.get('result', {}).get('file_paths', {}).values() if f])}")
    else:
        print(f"❌ Huge living room failed: {huge_response.status_code}")
    
    print("\n🔍 COMPARISON:")
    if tiny_response.status_code == 200 and huge_response.status_code == 200:
        tiny_id = tiny_data.get('result', {}).get('scene_id')
        huge_id = huge_data.get('result', {}).get('scene_id')
        print(f"Tiny bathroom: {tiny_id}")
        print(f"Huge living room: {huge_id}")
        
        if tiny_id != huge_id:
            print("✅ DYNAMIC GENERATION WORKING! Different models created!")
        else:
            print("❌ Same models generated")
            
        # Show download URLs
        tiny_obj = tiny_data.get('result', {}).get('obj_file')
        huge_obj = huge_data.get('result', {}).get('obj_file')
        print(f"\n📥 Download URLs:")
        print(f"Tiny: http://localhost:3000{tiny_obj}")
        print(f"Huge: http://localhost:3000{huge_obj}")

if __name__ == "__main__":
    test_api_with_different_rooms()
