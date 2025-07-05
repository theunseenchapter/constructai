# 🏗️ ConstructAI: Complete AI-Powered Construction Management System

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [High-Level Architecture](#high-level-architecture)
3. [Detailed Tech Stack](#detailed-tech-stack)
4. [7-Month Development Timeline](#7-month-development-timeline)
5. [Database Schema](#database-schema)
6. [API Endpoints](#api-endpoints)
7. [Setup Instructions](#setup-instructions)
8. [Deployment Guide](#deployment-guide)
9. [Open Source Datasets & Models](#open-source-datasets--models)
10. [Licensing](#licensing)

## 🎯 System Overview

ConstructAI is a completely **FREE** and deployable AI-powered construction management system that transforms how construction projects are planned, monitored, and executed.

### Core Modules:
1. **2D→3D Converter**: Blueprint to floor plan conversion using ControlNet + SAM
2. **BOQ & Cost Estimator**: Pandas-based rules engine with PDF/Excel export
3. **Vision Suite**: PPE detection, crack analysis, progress tracking
4. **MistriBot**: Multilingual local chatbot with voice capabilities
5. **Web Dashboard**: Next.js 14 PWA with real-time updates
6. **Mobile App**: React Native Expo for field operations
7. **Backend**: FastAPI microservices with MinIO + PostgreSQL
8. **AI Services**: TorchServe containers for model inference

## 🏛️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        ConstructAI System                       │
├─────────────────────────────────────────────────────────────────┤
│                     Frontend Layer                             │
│  ┌─────────────────────┐    ┌─────────────────────────────────┐ │
│  │   Next.js 14 PWA    │    │   React Native Expo App        │ │
│  │   - Dashboard       │    │   - Field Operations           │ │
│  │   - 3D Viewer       │    │   - Progress Tracking          │ │
│  │   - BOQ Management  │    │   - Safety Monitoring          │ │
│  │   - Chat Interface  │    │   - Voice Interface            │ │
│  └─────────────────────┘    └─────────────────────────────────┘ │
│                     │                        │                  │
│                     └────────────────────────┘                  │
│                              │                                  │
├─────────────────────────────────────────────────────────────────┤
│                     API Gateway                                 │
│                    (FastAPI + NGINX)                           │
├─────────────────────────────────────────────────────────────────┤
│                  Microservices Layer                           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐ │
│  │   User      │ │  Project    │ │   Vision    │ │  Chatbot  │ │
│  │  Service    │ │  Service    │ │  Service    │ │  Service  │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └───────────┘ │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐ │
│  │    BOQ      │ │   File      │ │ Notification│ │  3D Conv  │ │
│  │  Service    │ │  Service    │ │  Service    │ │  Service  │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └───────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                   AI Services Layer                            │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐ │
│  │  TorchServe │ │  TorchServe │ │  TorchServe │ │  Local    │ │
│  │   YOLOv8    │ │ DeepCrack   │ │ ControlNet  │ │   LLM     │ │
│  │    PPE      │ │   Cracks    │ │   SAM       │ │  Phi-3    │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └───────────┘ │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐ │
│  │  Whisper    │ │  Coqui TTS  │ │  Siamese    │ │  Three.js │ │
│  │     STT     │ │   Voice     │ │    CNN      │ │  Renderer │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └───────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                    Storage Layer                               │
│  ┌─────────────────────┐         ┌─────────────────────────────┐ │
│  │     PostgreSQL      │         │         MinIO               │ │
│  │   - User data       │         │   - Blueprints             │ │
│  │   - Projects        │         │   - 3D models              │ │
│  │   - BOQ records     │         │   - Images/Videos          │ │
│  │   - Progress logs   │         │   - Generated reports      │ │
│  └─────────────────────┘         └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 🛠️ Detailed Tech Stack

| Layer | Technology | Purpose | License | Cost |
|-------|------------|---------|---------|------|
| **Frontend** |
| Framework | Next.js 14 | React-based web framework | MIT | Free |
| Mobile | React Native + Expo | Cross-platform mobile | MIT | Free |
| UI Library | shadcn/ui + Tailwind CSS | Component library | MIT | Free |
| 3D Rendering | Three.js + expo-three | 3D visualization | MIT | Free |
| State Management | Zustand | Lightweight state manager | MIT | Free |
| **Backend** |
| API Framework | FastAPI | High-performance Python API | MIT | Free |
| API Gateway | NGINX | Load balancer & reverse proxy | BSD | Free |
| Authentication | FastAPI-Users | User management | MIT | Free |
| **AI/ML** |
| Model Serving | TorchServe | PyTorch model serving | Apache 2.0 | Free |
| Computer Vision | YOLOv8 | Object detection | AGPL-3.0 | Free |
| Crack Detection | DeepCrack | Crack segmentation | MIT | Free |
| 2D→3D | ControlNet + SAM | Image-to-3D conversion | Apache 2.0 | Free |
| LLM | Phi-3 Mini (3.8B) | Local language model | MIT | Free |
| STT | Whisper.cpp | Speech recognition | MIT | Free |
| TTS | Coqui TTS | Text-to-speech | MPL-2.0 | Free |
| **Data** |
| Database | PostgreSQL | Relational database | PostgreSQL | Free |
| File Storage | MinIO | S3-compatible storage | AGPL-3.0 | Free |
| Vector DB | pgvector | Vector embeddings | PostgreSQL | Free |
| **Infrastructure** |
| Containerization | Docker + Docker Compose | Container orchestration | Apache 2.0 | Free |
| Message Queue | Redis | Caching & pub/sub | BSD | Free |
| Monitoring | Prometheus + Grafana | Metrics & visualization | Apache 2.0 | Free |
| **Development** |
| Language | TypeScript | Type-safe development | Apache 2.0 | Free |
| Testing | Jest + Playwright | Unit & E2E testing | MIT | Free |
| Linting | ESLint + Prettier | Code quality | MIT | Free |

## 📅 7-Month Development Timeline

### **Month 1: Foundation & Core Infrastructure**
**Week 1-2: Project Setup**
- [ ] Set up monorepo structure with shared TypeScript types
- [ ] Configure Docker Compose for local development
- [ ] Set up PostgreSQL with initial schema
- [ ] Create basic FastAPI gateway with authentication

**Week 3-4: Core Services**
- [ ] Implement User Service (registration, login, profiles)
- [ ] Set up MinIO for file storage
- [ ] Create File Service for upload/download
- [ ] Implement basic project management

### **Month 2: Frontend Foundation**
**Week 1-2: Next.js Setup**
- [ ] Create responsive dashboard layout
- [ ] Implement authentication flow
- [ ] Set up shadcn/ui component library
- [ ] Create project management interface

**Week 3-4: Mobile App Foundation**
- [ ] Set up React Native Expo project
- [ ] Create shared component library
- [ ] Implement camera integration
- [ ] Basic navigation and authentication

### **Month 3: 2D→3D Conversion Module**
**Week 1-2: ControlNet Setup**
- [ ] Set up TorchServe container
- [ ] Implement ControlNet for edge detection
- [ ] Integrate Segment Anything Model (SAM)
- [ ] Create blueprint preprocessing pipeline

**Week 3-4: 3D Generation**
- [ ] Implement depth map generation
- [ ] Create glTF export functionality
- [ ] Integrate Three.js viewer
- [ ] Add 3D model manipulation tools

### **Month 4: BOQ & Cost Estimation**
**Week 1-2: Rules Engine**
- [ ] Create Pandas-based calculation engine
- [ ] Implement material cost database
- [ ] Set up regional pricing variations
- [ ] Create quantity calculation algorithms

**Week 3-4: Report Generation**
- [ ] Implement PDF generation with ReportLab
- [ ] Create Excel export functionality
- [ ] Design cost breakdown templates
- [ ] Add cost optimization suggestions

### **Month 5: Computer Vision Suite**
**Week 1-2: PPE Detection**
- [ ] Fine-tune YOLOv8 for construction PPE
- [ ] Implement real-time detection pipeline
- [ ] Create safety compliance dashboard
- [ ] Add alert system for violations

**Week 3-4: Progress & Quality Monitoring**
- [ ] Implement DeepCrack for structural analysis
- [ ] Create Siamese CNN for progress tracking
- [ ] Build comparison interface with BIM models
- [ ] Add automated progress reporting

### **Month 6: MistriBot - Local AI Assistant**
**Week 1-2: Language Model Setup**
- [ ] Deploy Phi-3 Mini with Ollama
- [ ] Create construction domain fine-tuning
- [ ] Implement context-aware responses
- [ ] Add multilingual support (English, Hindi, Spanish)

**Week 3-4: Voice Interface**
- [ ] Integrate Whisper.cpp for STT
- [ ] Set up Coqui TTS for voice responses
- [ ] Create hands-free voice commands
- [ ] Implement voice-based data entry

### **Month 7: Integration & Deployment**
**Week 1-2: System Integration**
- [ ] Connect all microservices
- [ ] Implement real-time notifications
- [ ] Add comprehensive error handling
- [ ] Create automated testing suite

**Week 3-4: Deployment & Documentation**
- [ ] Create Fly.io deployment configuration
- [ ] Set up Render free-tier alternative
- [ ] Write comprehensive documentation
- [ ] Create demo environment

## 🗄️ Database Schema

```sql
-- Users and Authentication
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'user',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Projects
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    owner_id UUID REFERENCES users(id),
    status VARCHAR(50) DEFAULT 'planning',
    budget DECIMAL(15,2),
    start_date DATE,
    end_date DATE,
    location JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Files and Documents
CREATE TABLE files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id),
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50),
    file_size BIGINT,
    minio_path VARCHAR(500),
    upload_by UUID REFERENCES users(id),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- BOQ (Bill of Quantities)
CREATE TABLE boq_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id),
    item_code VARCHAR(100),
    description TEXT NOT NULL,
    unit VARCHAR(50),
    quantity DECIMAL(10,3),
    unit_rate DECIMAL(10,2),
    total_amount DECIMAL(15,2),
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3D Models
CREATE TABLE models_3d (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id),
    source_file_id UUID REFERENCES files(id),
    model_path VARCHAR(500),
    model_type VARCHAR(50), -- 'blueprint_conversion', 'bim', 'scan'
    conversion_params JSONB,
    status VARCHAR(50) DEFAULT 'processing',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Computer Vision Analysis
CREATE TABLE cv_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id),
    source_file_id UUID REFERENCES files(id),
    analysis_type VARCHAR(50), -- 'ppe_detection', 'crack_analysis', 'progress_tracking'
    results JSONB,
    confidence_score DECIMAL(5,4),
    reviewed_by UUID REFERENCES users(id),
    status VARCHAR(50) DEFAULT 'pending_review',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Progress Tracking
CREATE TABLE progress_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id),
    log_date DATE NOT NULL,
    progress_percentage DECIMAL(5,2),
    completion_details JSONB,
    photos JSONB, -- Array of file IDs
    logged_by UUID REFERENCES users(id),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chat Conversations
CREATE TABLE chat_conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    project_id UUID REFERENCES projects(id),
    conversation_title VARCHAR(255),
    language VARCHAR(10) DEFAULT 'en',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES chat_conversations(id),
    role VARCHAR(20), -- 'user', 'assistant'
    content TEXT NOT NULL,
    message_type VARCHAR(50) DEFAULT 'text', -- 'text', 'voice', 'image'
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Notifications
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(50), -- 'info', 'warning', 'error', 'success'
    is_read BOOLEAN DEFAULT false,
    action_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Vector embeddings for semantic search
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE document_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    file_id UUID REFERENCES files(id),
    chunk_index INTEGER,
    content_chunk TEXT,
    embedding vector(1536),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ON document_embeddings USING ivfflat (embedding vector_cosine_ops);
```

## 🔗 API Endpoints

### Authentication Service
```typescript
POST   /auth/register          // User registration
POST   /auth/login             // User login
POST   /auth/refresh           // Token refresh
POST   /auth/logout            // User logout
GET    /auth/me                // Current user info
```

### Project Service
```typescript
GET    /projects               // List user projects
POST   /projects               // Create new project
GET    /projects/{id}          // Get project details
PUT    /projects/{id}          // Update project
DELETE /projects/{id}          // Delete project
GET    /projects/{id}/members  // Project team members
POST   /projects/{id}/members  // Add team member
```

### File Service
```typescript
POST   /files/upload           // Upload file
GET    /files/{id}             // Download file
DELETE /files/{id}             // Delete file
GET    /files/{id}/metadata    // File metadata
POST   /files/{id}/process     // Trigger AI processing
```

### 3D Conversion Service
```typescript
POST   /3d/convert-blueprint   // Convert 2D to 3D
GET    /3d/models/{id}         // Get 3D model
GET    /3d/models/{id}/preview // Get model preview
POST   /3d/models/{id}/export  // Export model (glTF, etc.)
```

### BOQ Service
```typescript
GET    /boq/{project_id}       // Get project BOQ
POST   /boq/{project_id}/items // Add BOQ item
PUT    /boq/items/{id}         // Update BOQ item
DELETE /boq/items/{id}         // Delete BOQ item
POST   /boq/{project_id}/calculate // Recalculate costs
GET    /boq/{project_id}/export // Export BOQ (PDF/Excel)
```

### Vision Service
```typescript
POST   /vision/analyze-ppe     // PPE detection
POST   /vision/detect-cracks   // Crack detection
POST   /vision/track-progress  // Progress analysis
GET    /vision/analysis/{id}   // Get analysis results
POST   /vision/batch-process   // Batch image processing
```

### Chatbot Service
```typescript
POST   /chat/conversations     // Create conversation
GET    /chat/conversations     // List conversations
POST   /chat/conversations/{id}/messages // Send message
GET    /chat/conversations/{id}/messages // Get chat history
POST   /chat/voice             // Voice message processing
```

## 🚀 Setup Instructions

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- Docker and Docker Compose
- Git

### Local Development Setup

1. **Clone and Setup Project**
```bash
git clone <repository-url>
cd constructai
npm install
```

2. **Environment Configuration**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Start Services**
```bash
# Start all services
docker-compose up -d

# Start frontend
npm run dev

# Start mobile app
cd mobile && npm run start
```

### Docker Compose Configuration

```yaml
version: '3.8'

services:
  # Database
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: constructai
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"

  # Object Storage
  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
    environment:
      MINIO_ACCESS_KEY: minioadmin
      MINIO_SECRET_KEY: minioadmin123
    volumes:
      - minio_data:/data
    ports:
      - "9000:9000"
      - "9001:9001"

  # Redis for caching
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  # API Gateway
  api-gateway:
    build:
      context: ./backend/gateway
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://admin:password@postgres:5432/constructai
      - REDIS_URL=redis://redis:6379
      - MINIO_URL=http://minio:9000
    depends_on:
      - postgres
      - redis
      - minio

  # AI Services
  torchserve-vision:
    build:
      context: ./ai-services/vision
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
      - "8081:8081"
    volumes:
      - ./models:/models
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  # Local LLM Service
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

volumes:
  postgres_data:
  minio_data:
  ollama_data:
```

## 🌐 Deployment Guide

### Fly.io Deployment (Recommended for Free Tier)

1. **Install Fly CLI**
```bash
# Windows
iwr https://fly.io/install.ps1 -useb | iex

# macOS/Linux
curl -L https://fly.io/install.sh | sh
```

2. **Deploy Services**
```bash
# Login to Fly.io
fly auth login

# Deploy API Gateway
cd backend/gateway
fly launch --no-deploy
fly deploy

# Deploy Frontend
cd ../../frontend
fly launch --no-deploy
fly deploy
```

### Render.com Alternative

```yaml
# render.yaml
services:
  - type: web
    name: constructai-frontend
    env: node
    plan: free
    buildCommand: npm run build
    startCommand: npm start
    envVars:
      - key: NODE_ENV
        value: production

  - type: web
    name: constructai-backend
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT

databases:
  - name: constructai-db
    plan: free
    databaseName: constructai
```

## 📊 Open Source Datasets & Models

### Computer Vision Models
| Model | Purpose | Download Link | License |
|-------|---------|---------------|---------|
| YOLOv8 | PPE Detection | [Ultralytics Hub](https://github.com/ultralytics/ultralytics) | AGPL-3.0 |
| SAM | Image Segmentation | [Meta Research](https://github.com/facebookresearch/segment-anything) | Apache 2.0 |
| ControlNet | Image-to-Image | [HuggingFace](https://huggingface.co/lllyasviel/ControlNet) | Apache 2.0 |
| DeepCrack | Crack Detection | [GitHub](https://github.com/yhlleo/DeepCrack) | MIT |

### Language Models
| Model | Size | Purpose | Download Link |
|-------|------|---------|---------------|
| Phi-3 Mini | 3.8B | Local Chat | [HuggingFace](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct) |
| Whisper Base | 74M | Speech-to-Text | [OpenAI](https://github.com/openai/whisper) |
| Coqui TTS | - | Text-to-Speech | [Coqui AI](https://github.com/coqui-ai/TTS) |

### Datasets
| Dataset | Purpose | Size | Link |
|---------|---------|------|------|
| COCO | Object Detection | 2.5GB | [COCO Dataset](https://cocodataset.org/) |
| Construction Images | PPE Training | 1.2GB | [Roboflow](https://roboflow.com/browse/construction-safety) |
| Crack500 | Crack Detection | 500MB | [GitHub](https://github.com/fyangneil/pavement-crack-detection) |
| FloorPlan Dataset | 2D→3D Training | 2GB | [Papers With Code](https://paperswithcode.com/dataset/rplan) |

## 📝 Licensing

All components are carefully selected to ensure **100% free and open-source** usage:

### ✅ Permissive Licenses (Commercial Use Allowed)
- **MIT**: Next.js, React, TypeScript, Three.js, Whisper
- **Apache 2.0**: FastAPI, ControlNet, SAM, TorchServe
- **BSD**: PostgreSQL, NGINX

### ⚠️ Copyleft Licenses (Source Available)
- **AGPL-3.0**: YOLOv8, MinIO (Commercial licenses available if needed)
- **MPL-2.0**: Coqui TTS

### 📋 Compliance Notes
1. **AGPL Components**: Source code must be made available if modified
2. **Attribution**: Proper attribution required for all components
3. **No Restrictions**: Can be used commercially without licensing fees
4. **Distribution**: Include license files when distributing

## 🎯 Quick Start Commands

### Frontend Setup
```bash
# Install dependencies
npm install

# Add required packages
npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu
npm install lucide-react class-variance-authority clsx tailwind-merge
npm install three @types/three expo-three
npm install zustand axios socket.io-client

# Start development server
npm run dev
```

### Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary
pip install torch torchvision torchaudio transformers
pip install opencv-python ultralytics
pip install pandas openpyxl reportlab
pip install minio redis python-multipart

# Start FastAPI server
uvicorn main:app --reload
```

### Mobile Setup
```bash
# Install Expo CLI
npm install -g @expo/cli

# Create Expo project
npx create-expo-app mobile --template blank-typescript

# Start development
cd mobile && npm start
```

This comprehensive system provides a complete, production-ready AI construction management platform that can be deployed for free using the specified tech stack and deployment options.
