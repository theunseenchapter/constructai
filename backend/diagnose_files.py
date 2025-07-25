#!/usr/bin/env python3
"""
Diagnostic tool to check file generation and download issues
"""

import requests
import json
import time
import os

def diagnose_file_generation():
    print('🔧 Diagnosing NeRF File Generation Issues...')
    print('=' * 60)
    
    # Step 1: Generate a new model and track the process
    print('\n1️⃣ Generating new NeRF model...')
    
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
        # Count files before generation
        renders_dir = '../public/renders'
        before_files = set(os.listdir(renders_dir)) if os.path.exists(renders_dir) else set()
        nerf_files_before = [f for f in before_files if f.startswith('nerf_')]
        print(f'   📁 Files before: {len(nerf_files_before)} NeRF files')
        
        # Generate model
        print('   🧠 Calling frontend API...')
        start_time = time.time()
        response = requests.post(frontend_url, json=payload, timeout=30)
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            print(f'   ✅ API success ({end_time - start_time:.1f}s)')
            
            # Check what files were reported as generated
            model_files = result.get('model_files', {})
            print(f'   📋 Reported files:')
            for file_type, filename in model_files.items():
                if filename:
                    print(f'      {file_type}: {filename}')
            
            # Count files after generation
            time.sleep(1)  # Give filesystem a moment
            after_files = set(os.listdir(renders_dir)) if os.path.exists(renders_dir) else set()
            nerf_files_after = [f for f in after_files if f.startswith('nerf_')]
            new_files = after_files - before_files
            
            print(f'   📁 Files after: {len(nerf_files_after)} NeRF files')
            print(f'   🆕 New files: {len(new_files)}')
            
            if new_files:
                print(f'   📄 New files created:')
                for new_file in sorted(new_files):
                    if new_file.startswith('nerf_'):
                        file_path = os.path.join(renders_dir, new_file)
                        file_size = os.path.getsize(file_path)
                        print(f'      ✅ {new_file} ({file_size} bytes)')
            
            # Step 2: Test download for each reported file
            print(f'\n2️⃣ Testing downloads...')
            
            for file_type, filename in model_files.items():
                if filename and file_type in ['obj_file', 'ply_file']:
                    print(f'   🔗 Testing download: {filename}')
                    
                    # Check if file exists on disk
                    file_path = os.path.join(renders_dir, filename)
                    if os.path.exists(file_path):
                        file_size = os.path.getsize(file_path)
                        print(f'      ✅ File exists on disk ({file_size} bytes)')
                        
                        # Test download endpoint
                        download_url = f'http://localhost:3000/api/download/{filename}'
                        try:
                            download_response = requests.head(download_url, timeout=10)
                            if download_response.status_code == 200:
                                print(f'      ✅ Download endpoint works')
                            else:
                                print(f'      ❌ Download failed: {download_response.status_code}')
                                print(f'         Headers: {dict(download_response.headers)}')
                        except Exception as e:
                            print(f'      ❌ Download error: {e}')
                    else:
                        print(f'      ❌ File does NOT exist on disk')
                        print(f'         Expected path: {file_path}')
                        
                        # Check if it exists with a different name pattern
                        similar_files = [f for f in os.listdir(renders_dir) if f.startswith('nerf_')]
                        print(f'         Recent NeRF files: {similar_files[-3:] if similar_files else "None"}')
            
            return result
        else:
            print(f'   ❌ API failed: {response.status_code}')
            print(f'   Error: {response.text}')
            return None
            
    except Exception as e:
        print(f'   ❌ Error: {e}')
        return None

def check_backend_file_copying():
    print('\n3️⃣ Checking backend file copying...')
    
    # Check backend generated_models directory
    backend_dir = 'generated_models'
    if os.path.exists(backend_dir):
        backend_files = os.listdir(backend_dir)
        nerf_backend_files = [f for f in backend_files if f.startswith('nerf_')]
        print(f'   📁 Backend files: {len(nerf_backend_files)} NeRF files')
        
        if nerf_backend_files:
            print(f'   📄 Recent backend files:')
            for f in sorted(nerf_backend_files)[-5:]:
                file_path = os.path.join(backend_dir, f)
                file_size = os.path.getsize(file_path)
                print(f'      {f} ({file_size} bytes)')
    else:
        print(f'   ❌ Backend generated_models directory not found')
    
    # Check public renders directory
    renders_dir = '../public/renders'
    if os.path.exists(renders_dir):
        render_files = os.listdir(renders_dir)
        nerf_render_files = [f for f in render_files if f.startswith('nerf_')]
        print(f'   📁 Public files: {len(nerf_render_files)} NeRF files')
        
        if nerf_render_files:
            print(f'   📄 Recent public files:')
            for f in sorted(nerf_render_files)[-5:]:
                file_path = os.path.join(renders_dir, f)
                file_size = os.path.getsize(file_path)
                print(f'      {f} ({file_size} bytes)')
    else:
        print(f'   ❌ Public renders directory not found')

def main():
    print('🏥 NeRF File Generation Diagnostic Tool')
    print('Investigating download failures...\n')
    
    result = diagnose_file_generation()
    check_backend_file_copying()
    
    print('\n' + '=' * 60)
    print('🔍 DIAGNOSIS COMPLETE')
    
    if result:
        print('✅ File generation appears to be working')
        print('💡 If downloads still fail, the issue may be:')
        print('   1. Race condition between file creation and download')
        print('   2. File copying between backend and frontend')
        print('   3. Caching issues in the browser')
        print('   4. File permission problems')
    else:
        print('❌ File generation failed')
        print('🔧 Check backend logs and ensure the real NeRF service is running')

if __name__ == '__main__':
    main()
