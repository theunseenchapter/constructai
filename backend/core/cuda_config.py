"""
CUDA Configuration for ConstructAI
Optimized for CUDA 12.1 installation
"""

import os
import torch
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CUDAConfig:
    """CUDA configuration and optimization for ConstructAI"""
    
    def __init__(self):
        self.cuda_version = "12.1"
        self.device = None
        self.gpu_memory_gb = None
        self.compute_capability = None
        self.initialize_cuda()
    
    def initialize_cuda(self):
        """Initialize CUDA settings and check GPU availability"""
        try:
            # Check CUDA availability
            if torch.cuda.is_available():
                self.device = torch.device("cuda")
                device_count = torch.cuda.device_count()
                current_device = torch.cuda.current_device()
                
                # Get GPU properties
                gpu_props = torch.cuda.get_device_properties(current_device)
                self.gpu_memory_gb = gpu_props.total_memory / (1024**3)
                self.compute_capability = f"{gpu_props.major}.{gpu_props.minor}"
                
                logger.info(f"🚀 CUDA {self.cuda_version} initialized successfully!")
                logger.info(f"📱 GPU Device: {gpu_props.name}")
                logger.info(f"💾 GPU Memory: {self.gpu_memory_gb:.1f} GB")
                logger.info(f"🔧 Compute Capability: {self.compute_capability}")
                logger.info(f"🎯 Available GPUs: {device_count}")
                
                # Optimize CUDA settings
                self.optimize_cuda_settings()
                
            else:
                self.device = torch.device("cpu")
                logger.warning("⚠️ CUDA not available, using CPU")
                
        except Exception as e:
            logger.error(f"❌ CUDA initialization failed: {e}")
            self.device = torch.device("cpu")
    
    def optimize_cuda_settings(self):
        """Optimize CUDA settings for ConstructAI workloads"""
        try:
            # Enable CUDA optimizations
            torch.backends.cudnn.enabled = True
            torch.backends.cudnn.benchmark = True  # Optimize for consistent input sizes
            torch.backends.cudnn.deterministic = False  # Allow non-deterministic algorithms for speed
            
            # Set memory allocation strategy
            os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:512'
            
            # Enable Tensor Core usage for mixed precision
            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True
            
            logger.info("✅ CUDA optimizations enabled")
            
        except Exception as e:
            logger.error(f"❌ CUDA optimization failed: {e}")
    
    def get_optimal_batch_size(self, model_type: str = "nerf") -> int:
        """Calculate optimal batch size based on GPU memory"""
        if self.device.type == "cpu":
            return 1
        
        # Batch size recommendations based on GPU memory and model type
        memory_gb = self.gpu_memory_gb or 4
        
        batch_sizes = {
            "nerf": {
                4: 1024,    # RTX 3060 4GB
                6: 2048,    # RTX 3060 6GB  
                8: 4096,    # RTX 3070 8GB
                10: 6144,   # RTX 3080 10GB
                12: 8192,   # RTX 3080 Ti 12GB
                16: 12288,  # RTX 4080 16GB
                24: 16384,  # RTX 4090 24GB
            },
            "blender": {
                4: 2,
                6: 4,
                8: 6,
                10: 8,
                12: 12,
                16: 16,
                24: 24,
            },
            "vision": {
                4: 8,
                6: 16,
                8: 32,
                10: 48,
                12: 64,
                16: 96,
                24: 128,
            }
        }
        
        # Find closest memory size
        memory_options = sorted(batch_sizes[model_type].keys())
        closest_memory = min(memory_options, key=lambda x: abs(x - memory_gb))
        
        return batch_sizes[model_type][closest_memory]
    
    def get_device_info(self) -> dict:
        """Get comprehensive device information"""
        info = {
            "device": str(self.device),
            "cuda_available": torch.cuda.is_available(),
            "cuda_version": self.cuda_version,
            "pytorch_version": torch.__version__,
        }
        
        if torch.cuda.is_available():
            info.update({
                "gpu_name": torch.cuda.get_device_name(),
                "gpu_memory_gb": self.gpu_memory_gb,
                "compute_capability": self.compute_capability,
                "gpu_count": torch.cuda.device_count(),
                "current_gpu": torch.cuda.current_device(),
            })
            
        return info
    
    def clear_cache(self):
        """Clear CUDA cache to free memory"""
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            logger.info("🧹 CUDA cache cleared")

# Global CUDA configuration instance
cuda_config = CUDAConfig()

# Export commonly used values
DEVICE = cuda_config.device
GPU_AVAILABLE = torch.cuda.is_available()
OPTIMAL_NERF_BATCH_SIZE = cuda_config.get_optimal_batch_size("nerf")
OPTIMAL_VISION_BATCH_SIZE = cuda_config.get_optimal_batch_size("vision")

def get_device():
    """Get the optimal device for computation"""
    return DEVICE

def get_gpu_info():
    """Get GPU information"""
    return cuda_config.get_device_info()

def clear_gpu_cache():
    """Clear GPU memory cache"""
    cuda_config.clear_cache()

# Print initialization info
if __name__ == "__main__":
    info = cuda_config.get_device_info()
    print("🎯 CUDA Configuration:")
    for key, value in info.items():
        print(f"  {key}: {value}")
