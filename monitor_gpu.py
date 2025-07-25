#!/usr/bin/env python3
"""
GPU Usage Monitor for ConstructAI
Monitor NVIDIA RTX 4050 usage during 3D rendering
"""
import time
import subprocess
import sys

def monitor_gpu_usage():
    print("🔍 Monitoring NVIDIA RTX 4050 GPU usage...")
    print("Watch Task Manager to see GPU 1 usage increase!")
    print("Press Ctrl+C to stop monitoring")
    
    try:
        while True:
            try:
                # Run nvidia-smi to get GPU usage
                result = subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu', '--format=csv,noheader,nounits'], 
                                      capture_output=True, text=True, timeout=5)
                
                if result.returncode == 0:
                    gpu_data = result.stdout.strip().split(', ')
                    gpu_util = gpu_data[0]
                    mem_used = gpu_data[1]
                    mem_total = gpu_data[2]
                    temp = gpu_data[3]
                    
                    print(f"\r🚀 NVIDIA RTX 4050: {gpu_util}% GPU | {mem_used}/{mem_total}MB VRAM | {temp}°C", end='', flush=True)
                else:
                    print(f"\r❌ GPU monitoring failed", end='', flush=True)
                    
            except subprocess.TimeoutExpired:
                print(f"\r⏰ Monitoring timeout", end='', flush=True)
            except Exception as e:
                print(f"\r❌ Monitor error: {e}", end='', flush=True)
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\n\n✅ GPU monitoring stopped")

if __name__ == "__main__":
    monitor_gpu_usage()
