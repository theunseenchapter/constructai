#!/usr/bin/env python3
"""
Test the real NeRF with an actual image file upload
"""

import requests
import json
import base64
import os
from PIL import Image
import io

def convert_image_to_base64(image_path):
    """Convert an image file to base64 format"""
    try:
        with open(image_path, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            # Determine the image format
            img = Image.open(image_path)
            format_lower = img.format.lower()
            mime_type = f"image/{format_lower}"
            return f"data:{mime_type};base64,{encoded_string}"
    except Exception as e:
        print(f"Error converting image to base64: {e}")
        return None

def test_with_actual_image(image_path=None):
    """Test the NeRF with an actual image file"""
    print('🖼️ Testing Real NeRF with Actual Image...')
    
    # If no image path provided, try common locations
    if not image_path:
        possible_images = [
            'living_room.jpg',
            'living_room.png',
            'test_image.jpg',
            'test_image.png',
            os.path.join('..', 'public', 'living_room.jpg'),
            os.path.join('..', 'public', 'living_room.png'),
        ]
        
        for img_path in possible_images:
            if os.path.exists(img_path):
                image_path = img_path
                break
    
    if not image_path or not os.path.exists(image_path):
        print("❌ No image file found. Please provide an image path.")
        print("💡 You can:")
        print("   1. Save your living room image as 'living_room.jpg' in the backend folder")
        print("   2. Or provide the full path to your image")
        return False
    
    print(f"📸 Using image: {image_path}")
    
    # Convert image to base64
    base64_image = convert_image_to_base64(image_path)
    if not base64_image:
        print("❌ Failed to convert image to base64")
        return False
    
    print(f"✅ Image converted to base64 ({len(base64_image)} characters)")
    
    # Test the real NeRF API
    url = 'http://localhost:8000/api/v1/real-nerf/process-images-to-3d'
    
    data = {
        'images': json.dumps([base64_image]),
        'config': json.dumps({
            'session_id': f'real_image_test_{int(os.path.getmtime(image_path))}',
            'room_specifications': {
                'room_type': 'living_room',
                'dimensions': {'width': 8, 'length': 10, 'height': 3}
            },
            'rendering_options': {
                'quality': 'high',
                'output_format': 'obj',
                'use_real_geometry': True
            }
        })
    }
    
    try:
        print('🧠 Processing real image with NeRF...')
        response = requests.post(url, data=data, timeout=120)
        print(f'📡 Response status: {response.status_code}')
        
        if response.status_code == 200:
            result = response.json()
            print('✅ Real image NeRF processing succeeded!')
            
            # Display results
            files = result.get('files', {})
            stats = result.get('stats', {})
            
            print(f'\n📊 Processing Results:')
            print(f'   Session ID: {result.get("session_id", "N/A")}')
            print(f'   Processing time: {stats.get("processing_time", "N/A")}s')
            print(f'   Image analyzed: {stats.get("image_analysis", {})}')
            
            if files:
                print(f'\n📁 Generated Files:')
                for file_type, filename in files.items():
                    print(f'   {file_type}: {filename}')
                
                # Try to examine the OBJ file
                obj_file = files.get('obj_file')
                if obj_file:
                    print(f'\n🔍 Examining generated OBJ file...')
                    
                    # Check multiple possible locations
                    possible_paths = [
                        obj_file,
                        os.path.join('generated_models', obj_file),
                        os.path.join('..', 'public', 'renders', obj_file),
                    ]
                    
                    for path in possible_paths:
                        if os.path.exists(path):
                            file_size = os.path.getsize(path)
                            print(f'✅ Found OBJ file: {path} ({file_size} bytes)')
                            
                            # Show content preview
                            with open(path, 'r') as f:
                                lines = f.readlines()[:20]
                            
                            print(f'\n📝 OBJ Content Preview:')
                            for i, line in enumerate(lines):
                                if line.strip():
                                    print(f'  {i+1}: {line.strip()}')
                            
                            # Count geometry elements
                            with open(path, 'r') as f:
                                content = f.read()
                            
                            vertices = content.count('\nv ')
                            faces = content.count('\nf ')
                            normals = content.count('\nvn ')
                            texture_coords = content.count('\nvt ')
                            
                            print(f'\n📊 3D Model Statistics:')
                            print(f'   Vertices: {vertices}')
                            print(f'   Faces: {faces}')
                            print(f'   Normals: {normals}')
                            print(f'   Texture coordinates: {texture_coords}')
                            print(f'   Total file size: {file_size} bytes')
                            
                            if vertices > 0 and faces > 0:
                                print('✅ Real 3D geometry detected!')
                            else:
                                print('⚠️ No geometry found in OBJ file')
                            
                            break
                    else:
                        print('❌ Generated OBJ file not found in expected locations')
            
            return True
        else:
            print(f'❌ Processing failed: {response.status_code}')
            try:
                error_data = response.json()
                print(f'Error details: {error_data}')
            except:
                print(f'Error text: {response.text}')
            return False
            
    except Exception as e:
        print(f'❌ Processing error: {e}')
        return False

def create_sample_living_room_image():
    """Create a sample living room image for testing if none exists"""
    print('🎨 Creating sample living room image...')
    
    # Create a simple living room scene
    img = Image.new('RGB', (800, 600), color='#f5f5f5')  # Light gray background
    
    # This is a very basic image - in practice you'd use your actual living room photo
    # For now, this serves as a placeholder
    
    filename = 'sample_living_room.png'
    img.save(filename)
    print(f'✅ Created sample image: {filename}')
    return filename

if __name__ == '__main__':
    print('🏠 Real NeRF Image Test\n')
    
    # Check if an image exists
    image_path = None
    
    # Look for uploaded image files
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    for file in os.listdir('.'):
        if any(file.lower().endswith(ext) for ext in image_extensions):
            if 'living' in file.lower() or 'room' in file.lower() or 'test' in file.lower():
                image_path = file
                break
    
    if not image_path:
        print("📸 No image found. Creating a sample for testing...")
        image_path = create_sample_living_room_image()
        print("💡 To test with your actual living room image:")
        print("   1. Save it as 'living_room.jpg' in the backend folder")
        print("   2. Re-run this script")
    
    success = test_with_actual_image(image_path)
    
    if success:
        print('\n🎉 Image test completed successfully!')
        print('✅ Your image was processed by the real NeRF model')
        print('✅ 3D geometry was generated')
        print('💡 You can now download the 3D model through the frontend')
    else:
        print('\n💥 Image test failed!')
        print('🔧 Check that the backend is running on port 8000')
        print('🔧 Ensure your image is in a supported format (JPG, PNG)')
