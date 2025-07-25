import subprocess
import sys
import os
import json

def find_blender():
    """Find Blender executable"""
    possible_paths = [
        r"D:\blender\blender.exe",
        r"C:\Program Files\Blender Foundation\Blender 4.4\blender.exe",
        r"C:\Program Files\Blender Foundation\Blender 4.3\blender.exe",
        r"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe",
        r"C:\Program Files\Blender Foundation\Blender 4.1\blender.exe",
        r"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe",
        "blender"  # If in PATH
    ]
    
    for path in possible_paths:
        if os.path.exists(path) or path == "blender":
            return path
    
    raise FileNotFoundError("Blender executable not found. Please install Blender or update the path.")

def run_colorful_floorplan_renderer(config_file):
    """Run the colorful floor plan renderer"""
    try:
        blender_path = find_blender()
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "colorful_floorplan_renderer.py")
        
        # Prepare the command
        cmd = [
            blender_path,
            "--background",
            "--python", script_path,
            "--", config_file
        ]
        
        print(f"🎨 Running colorful floor plan renderer with Blender: {blender_path}")
        print(f"📄 Config file: {config_file}")
        print(f"🔧 Command: {' '.join(cmd)}")
        
        # Set CUDA environment variables for GPU acceleration
        env = os.environ.copy()
        env['CUDA_VISIBLE_DEVICES'] = '0'  # Use first CUDA device
        env['CYCLES_CUDA_EXTRA_CFLAGS'] = '-O3'
        env['CYCLES_CUDA_BINARIES_ARCH'] = 'sm_75;sm_80;sm_86;sm_89'  # Support modern GPUs
        
        print(f"🚀 CUDA Environment: CUDA_VISIBLE_DEVICES={env.get('CUDA_VISIBLE_DEVICES', 'Not set')}")
        
        # Run the command with CUDA environment and UTF-8 encoding
        result = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=300, encoding='utf-8', errors='replace')
        
        print(f"🎯 Blender exit code: {result.returncode}")
        
        if result.stdout:
            print(f"📤 Blender stdout:\n{result.stdout}")
        
        if result.stderr:
            print(f"⚠️  Blender stderr:\n{result.stderr}")
        
        if result.returncode == 0:
            print("✅ Colorful floor plan generated successfully!")
            return True
        else:
            print(f"❌ Blender failed with exit code: {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Blender process timed out (5 minutes)")
        return False
    except Exception as e:
        print(f"❌ Error running Blender: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python colorful_floorplan_wrapper.py <config_file>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    success = run_colorful_floorplan_renderer(config_file)
    
    if not success:
        sys.exit(1)
