#!/usr/bin/env python3
"""
Quick test script for ConstructAI MCP integration
"""

import requests
import json
import time

def test_web_server():
    """Test if the web server is running"""
    try:
        response = requests.get('http://localhost:3001/api/health', timeout=5)
        if response.status_code == 200:
            print("✅ Web server is running on port 3001")
            return True
        else:
            print(f"❌ Web server responded with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Web server is not running: {e}")
        return False

def test_mcp_connection():
    """Test MCP server connection"""
    try:
        response = requests.post(
            'http://localhost:3001/api/mcp/connect',
            json={'server_url': 'http://localhost:9876'},
            timeout=10
        )
        if response.status_code == 200:
            print("✅ MCP server connection successful")
            return True
        else:
            print(f"❌ MCP connection failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ MCP connection test failed: {e}")
        return False

def test_scene_creation():
    """Test 3D scene creation"""
    try:
        scene_data = {
            "rooms": [
                {
                    "name": "Test Room",
                    "type": "living_room",
                    "width": 5,
                    "length": 6,
                    "height": 3
                }
            ],
            "building_dimensions": {
                "total_width": 5,
                "total_length": 6,
                "height": 3
            }
        }
        
        response = requests.post(
            'http://localhost:3001/api/mcp/create-scene',
            json=scene_data,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ 3D scene creation successful")
            return True
        else:
            print(f"❌ Scene creation failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Scene creation test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing ConstructAI MCP Integration\n")
    
    tests = [
        ("Web Server", test_web_server),
        ("MCP Connection", test_mcp_connection),
        ("Scene Creation", test_scene_creation)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        result = test_func()
        results.append(result)
        print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! ConstructAI is ready to use.")
        print("\n📋 Next steps:")
        print("1. Open http://localhost:3001/demo/modern-living-room")
        print("2. Try the Blender 3D demo")
        print("3. Use GitHub Copilot with @constructai-blender commands")
    else:
        print("❌ Some tests failed. Check the setup instructions.")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure 'npm run dev' is running")
        print("2. Check if MCP server is configured in VS Code")
        print("3. Verify Blender is installed and accessible")

if __name__ == "__main__":
    main()
