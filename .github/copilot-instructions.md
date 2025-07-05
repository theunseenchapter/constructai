# ConstructAI Copilot Instructions

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Overview
ConstructAI is a comprehensive AI-powered construction management system with the following key components:

- **Frontend**: Next.js 14 PWA with TypeScript and Tailwind CSS
- **Mobile**: React Native Expo app sharing TypeScript models
- **Backend**: FastAPI microservices architecture
- **AI Models**: Computer vision, NLP, and 3D conversion capabilities
- **Storage**: MinIO for files, PostgreSQL for metadata
- **Deployment**: Docker containers with GPU support

## Key Technologies
- TypeScript for type safety across frontend and backend
- FastAPI for high-performance Python APIs
- TorchServe for AI model serving
- Three.js for 3D visualization
- OpenCV and YOLOv8 for computer vision
- Whisper for speech-to-text
- Open-source LLMs (Phi-3 mini/Mistral 7B)

## Code Style Guidelines
- Use TypeScript strict mode
- Follow functional programming patterns where possible
- Implement proper error handling and logging
- Write comprehensive tests for critical components
- Use shadcn/ui components for consistent UI
- Follow REST API conventions for backend services

## Architecture Patterns
- Microservices for backend scalability
- Shared TypeScript types between frontend and backend
- Event-driven architecture for real-time updates
- Clean architecture with dependency injection
- Repository pattern for data access

## AI/ML Guidelines
- Use pre-trained models where possible to avoid training costs
- Implement model versioning and A/B testing
- Optimize models for edge deployment
- Use quantization for mobile deployment
- Implement proper model monitoring and fallbacks
