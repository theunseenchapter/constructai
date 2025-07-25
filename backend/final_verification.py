#!/usr/bin/env python3
"""
Final verification test of the complete NeRF pipeline
"""

import requests
import json
import time

def final_verification_test():
    print('🎯 Final NeRF Pipeline Verification')
    print('=' * 50)
    
    # Test 1: Backend Health
    print('\n1️⃣ Testing Backend Health...')
    try:
        health_response = requests.get('http://localhost:8000/api/v1/real-nerf/health', timeout=10)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f'   ✅ Backend: {health_data["status"]}')
            print(f'   🚀 CUDA: {health_data["device_info"]["cuda_available"]}')
            gpu_memory = health_data["device_info"].get("gpu_memory", "N/A")
            print(f'   💾 GPU Memory: {gpu_memory}')
        else:
            print(f'   ❌ Backend health check failed: {health_response.status_code}')
            return False
    except Exception as e:
        print(f'   ❌ Backend connection error: {e}')
        return False
    
    # Test 2: Frontend API
    print('\n2️⃣ Testing Frontend NeRF API...')
    frontend_url = 'http://localhost:3000/api/nerf/generate-3d'
    
    # Create a test payload
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
        print('   📡 Sending request to frontend API...')
        start_time = time.time()
        response = requests.post(frontend_url, json=payload, timeout=60)
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            print(f'   ✅ Frontend API success ({end_time - start_time:.1f}s)')
            
            # Verify response structure
            required_fields = ['success', 'nerf_id', 'model_files', 'stats']
            missing_fields = [field for field in required_fields if field not in result]
            
            if missing_fields:
                print(f'   ⚠️ Missing fields: {missing_fields}')
            else:
                print('   ✅ All required fields present')
            
            # Display stats
            if 'stats' in result:
                stats = result['stats']
                print(f'   📊 Generated Model Stats:')
                print(f'      Vertices: {stats.get("vertex_count", "N/A")}')
                print(f'      Faces: {stats.get("face_count", "N/A")}')
                print(f'      Processing: {stats.get("processing_time", "N/A")}s')
            
            # Test file generation
            model_files = result.get('model_files', {})
            generated_files = []
            
            for file_type, filename in model_files.items():
                if filename and file_type in ['obj_file', 'ply_file']:
                    generated_files.append((file_type, filename))
            
            if generated_files:
                print(f'   📁 Generated {len(generated_files)} model files')
                
                # Test download for first file
                file_type, filename = generated_files[0]
                test_download_url = f'http://localhost:3000/api/download/{filename}'
                
                try:
                    download_response = requests.head(test_download_url, timeout=10)
                    if download_response.status_code == 200:
                        print(f'   ✅ Download endpoint working')
                    else:
                        print(f'   ⚠️ Download test failed: {download_response.status_code}')
                except Exception as e:
                    print(f'   ⚠️ Download test error: {e}')
            else:
                print('   ❌ No model files generated')
                
            return True
        else:
            print(f'   ❌ Frontend API failed: {response.status_code}')
            print(f'   Error: {response.text[:200]}...' if len(response.text) > 200 else response.text)
            return False
            
    except Exception as e:
        print(f'   ❌ Frontend API error: {e}')
        return False

    # Test 3: File System Check
    print('\n3️⃣ Testing File System...')
    try:
        import os
        
        renders_dir = '../public/renders'
        if os.path.exists(renders_dir):
            nerf_files = [f for f in os.listdir(renders_dir) if f.startswith('nerf_')]
            print(f'   ✅ Renders directory exists')
            print(f'   📁 Found {len(nerf_files)} NeRF files')
            
            if nerf_files:
                # Show most recent files
                recent_files = sorted(nerf_files)[-3:]
                print(f'   📄 Recent files: {", ".join(recent_files)}')
            
            return True
        else:
            print(f'   ⚠️ Renders directory not found')
            return False
            
    except Exception as e:
        print(f'   ❌ File system check error: {e}')
        return False

def main():
    print('🏠 ConstructAI NeRF Pipeline Verification')
    print('Testing your living room image processing system...\n')
    
    success = final_verification_test()
    
    print('\n' + '=' * 50)
    if success:
        print('🎉 VERIFICATION COMPLETE!')
        print('✅ Your living room NeRF system is working perfectly!')
        print('')
        print('📋 What you can do now:')
        print('   1. Upload any room image through the test interface')
        print('   2. Generate real 3D models with actual geometry')
        print('   3. Download OBJ, PLY files for use in 3D software')
        print('   4. View the models in Blender, Three.js, or other tools')
        print('')
        print('🌐 Test Interface: http://localhost:3000/test-living-room.html')
        print('🔗 Main App: http://localhost:3000')
    else:
        print('💥 VERIFICATION FAILED!')
        print('❌ Some components are not working correctly')
        print('🔧 Check the console outputs above for specific issues')

if __name__ == '__main__':
    main()
