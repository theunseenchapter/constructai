#!/usr/bin/env python3
"""
CUDA 12.1 Test Script for ConstructAI
Tests PyTorch CUDA functionality and GPU acceleration
"""

import torch
import sys

def test_cuda_installation():
    """Test CUDA installation and GPU availability"""
    print("=" * 60)
    print("🚀 ConstructAI CUDA 12.1 Test Suite")
    print("=" * 60)
    
    # PyTorch version
    print(f"📦 PyTorch Version: {torch.__version__}")
    
    # CUDA availability
    cuda_available = torch.cuda.is_available()
    print(f"🎯 CUDA Available: {cuda_available}")
    
    if cuda_available:
        # CUDA version
        print(f"📊 CUDA Version: {torch.version.cuda}")
        
        # GPU count
        gpu_count = torch.cuda.device_count()
        print(f"🔢 GPU Count: {gpu_count}")
        
        # GPU details
        for i in range(gpu_count):
            gpu_name = torch.cuda.get_device_name(i)
            gpu_memory = torch.cuda.get_device_properties(i).total_memory / (1024**3)
            print(f"💾 GPU {i}: {gpu_name} ({gpu_memory:.1f} GB)")
        
        # Test tensor creation on GPU
        try:
            device = torch.device("cuda:0")
            test_tensor = torch.randn(1000, 1000, device=device)
            result = torch.mm(test_tensor, test_tensor.t())
            print(f"✅ GPU Tensor Operations: SUCCESS")
            print(f"🔥 Test Matrix Size: {result.shape}")
            
            # Memory usage
            allocated = torch.cuda.memory_allocated() / (1024**2)
            cached = torch.cuda.memory_reserved() / (1024**2)
            print(f"📈 GPU Memory - Allocated: {allocated:.1f} MB, Cached: {cached:.1f} MB")
            
        except Exception as e:
            print(f"❌ GPU Tensor Operations: FAILED - {e}")
        
        # CUDA capabilities
        major, minor = torch.cuda.get_device_capability()
        print(f"⚡ CUDA Compute Capability: {major}.{minor}")
        
    else:
        print("❌ CUDA not available - using CPU only")
        print("💡 Make sure NVIDIA drivers and CUDA 12.1 are properly installed")
    
    print("=" * 60)
    print("🏁 Test Complete")
    print("=" * 60)

if __name__ == "__main__":
    test_cuda_installation()
