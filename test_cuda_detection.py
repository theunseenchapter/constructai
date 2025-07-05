#!/usr/bin/env python3
"""
Test CUDA detection in Blender
"""
import subprocess
import os

def test_cuda_detection():
    """Test if Blender can detect CUDA devices"""
    blender_path = os.environ.get('BLENDER_PATH', 'D:\\blender\\blender.exe')
    
    cuda_test_script = '''
import bpy

print("🔍 Testing CUDA detection...")

# Get preferences
prefs = bpy.context.preferences
cprefs = prefs.addons['cycles'].preferences

print(f"Available compute device types: {[t for t in ['CUDA', 'OPENCL', 'OPTIX', 'HIP'] if hasattr(cprefs, 'compute_device_type')]}")

# Try to set CUDA
try:
    cprefs.compute_device_type = 'CUDA'
    print("✅ Successfully set compute device type to CUDA")
except Exception as e:
    print(f"❌ Failed to set CUDA: {e}")

# Refresh devices
cprefs.get_devices()

print(f"Total devices found: {len(cprefs.devices)}")

cuda_devices = []
for i, device in enumerate(cprefs.devices):
    print(f"Device {i}: {device.name} (Type: {device.type}, Use: {device.use})")
    if device.type == 'CUDA':
        cuda_devices.append(device)
        device.use = True

print(f"CUDA devices found: {len(cuda_devices)}")

if cuda_devices:
    print("🚀 CUDA devices available!")
    for device in cuda_devices:
        print(f"  - {device.name}")
else:
    print("❌ No CUDA devices found")
    
# Test render engine
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'GPU'

print(f"Render engine: {scene.render.engine}")
print(f"Cycles device: {scene.cycles.device}")
'''
    
    try:
        result = subprocess.run([
            blender_path,
            '--background',
            '--python-expr', cuda_test_script
        ], capture_output=True, text=True, timeout=60)
        
        print("CUDA Detection Test Output:")
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
            
    except Exception as e:
        print(f"Failed to run CUDA test: {e}")

if __name__ == "__main__":
    test_cuda_detection()
