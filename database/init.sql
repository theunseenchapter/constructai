-- ConstructAI Database Initialization Script
-- PostgreSQL with pgvector extension for vector embeddings

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "vector";

-- Users and Authentication
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'user' CHECK (role IN ('admin', 'manager', 'engineer', 'worker', 'user')),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Projects
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    owner_id UUID REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'planning' CHECK (status IN ('planning', 'active', 'paused', 'completed', 'cancelled')),
    budget DECIMAL(15,2),
    start_date DATE,
    end_date DATE,
    location JSONB,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Project team members
CREATE TABLE project_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) DEFAULT 'member',
    permissions JSONB DEFAULT '{}',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(project_id, user_id)
);

-- Files and Documents
CREATE TABLE files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50),
    file_size BIGINT,
    mime_type VARCHAR(100),
    minio_path VARCHAR(500),
    upload_by UUID REFERENCES users(id),
    metadata JSONB DEFAULT '{}',
    is_processed BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- BOQ (Bill of Quantities)
CREATE TABLE boq_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    item_code VARCHAR(100),
    description TEXT NOT NULL,
    unit VARCHAR(50),
    quantity DECIMAL(10,3),
    unit_rate DECIMAL(10,2),
    total_amount DECIMAL(15,2) GENERATED ALWAYS AS (quantity * unit_rate) STORED,
    category VARCHAR(100),
    subcategory VARCHAR(100),
    specifications JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cost estimation rules
CREATE TABLE cost_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rule_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    region VARCHAR(100),
    formula TEXT, -- Pandas calculation formula
    base_rates JSONB, -- Base material rates
    labor_rates JSONB, -- Labor cost rates
    overhead_percentage DECIMAL(5,2),
    profit_percentage DECIMAL(5,2),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3D Models
CREATE TABLE models_3d (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    source_file_id UUID REFERENCES files(id) ON DELETE CASCADE,
    model_path VARCHAR(500),
    model_type VARCHAR(50) CHECK (model_type IN ('blueprint_conversion', 'bim', 'scan')),
    conversion_params JSONB DEFAULT '{}',
    model_metadata JSONB DEFAULT '{}', -- vertices, faces, materials, etc.
    status VARCHAR(50) DEFAULT 'processing' CHECK (status IN ('processing', 'completed', 'failed')),
    error_message TEXT,
    processing_time INTEGER, -- seconds
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Computer Vision Analysis
CREATE TABLE cv_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    source_file_id UUID REFERENCES files(id) ON DELETE CASCADE,
    analysis_type VARCHAR(50) CHECK (analysis_type IN ('ppe_detection', 'crack_analysis', 'progress_tracking')),
    results JSONB NOT NULL,
    confidence_score DECIMAL(5,4),
    model_version VARCHAR(50),
    processing_time INTEGER, -- milliseconds
    reviewed_by UUID REFERENCES users(id),
    review_notes TEXT,
    status VARCHAR(50) DEFAULT 'pending_review' CHECK (status IN ('pending_review', 'approved', 'rejected')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP
);

-- Progress Tracking
CREATE TABLE progress_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    log_date DATE NOT NULL,
    progress_percentage DECIMAL(5,2),
    completion_details JSONB DEFAULT '{}',
    photos JSONB DEFAULT '[]', -- Array of file IDs
    weather_conditions JSONB,
    logged_by UUID REFERENCES users(id),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chat Conversations
CREATE TABLE chat_conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    project_id UUID REFERENCES projects(id) ON DELETE SET NULL,
    conversation_title VARCHAR(255),
    language VARCHAR(10) DEFAULT 'en' CHECK (language IN ('en', 'hi', 'es', 'fr')),
    model_name VARCHAR(100) DEFAULT 'phi-3-mini',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES chat_conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    message_type VARCHAR(50) DEFAULT 'text' CHECK (message_type IN ('text', 'voice', 'image', 'file')),
    metadata JSONB DEFAULT '{}',
    tokens_used INTEGER,
    processing_time INTEGER, -- milliseconds
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Notifications
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    project_id UUID REFERENCES projects(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(50) CHECK (type IN ('info', 'warning', 'error', 'success', 'alert')),
    priority VARCHAR(20) DEFAULT 'normal' CHECK (priority IN ('low', 'normal', 'high', 'urgent')),
    is_read BOOLEAN DEFAULT false,
    action_url VARCHAR(500),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_at TIMESTAMP
);

-- Safety incidents
CREATE TABLE safety_incidents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    reported_by UUID REFERENCES users(id),
    incident_date TIMESTAMP NOT NULL,
    incident_type VARCHAR(100), -- 'ppe_violation', 'accident', 'near_miss', etc.
    severity VARCHAR(20) CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    description TEXT NOT NULL,
    location_details TEXT,
    photos JSONB DEFAULT '[]',
    corrective_actions TEXT,
    resolved_by UUID REFERENCES users(id),
    status VARCHAR(50) DEFAULT 'open' CHECK (status IN ('open', 'investigating', 'resolved', 'closed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);

-- Vector embeddings for semantic search
CREATE TABLE document_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    file_id UUID REFERENCES files(id) ON DELETE CASCADE,
    chunk_index INTEGER,
    content_chunk TEXT,
    embedding vector(1536), -- OpenAI embedding size
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Model performance tracking
CREATE TABLE model_performance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50),
    task_type VARCHAR(50), -- 'ppe_detection', 'crack_analysis', etc.
    accuracy DECIMAL(5,4),
    precision_score DECIMAL(5,4),
    recall DECIMAL(5,4),
    f1_score DECIMAL(5,4),
    inference_time INTEGER, -- milliseconds
    dataset_size INTEGER,
    test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- API usage tracking
CREATE TABLE api_usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    endpoint VARCHAR(255) NOT NULL,
    method VARCHAR(10),
    status_code INTEGER,
    response_time INTEGER, -- milliseconds
    request_size INTEGER, -- bytes
    response_size INTEGER, -- bytes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_projects_owner ON projects(owner_id);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_files_project ON files(project_id);
CREATE INDEX idx_files_type ON files(file_type);
CREATE INDEX idx_boq_project ON boq_items(project_id);
CREATE INDEX idx_boq_category ON boq_items(category);
CREATE INDEX idx_models_project ON models_3d(project_id);
CREATE INDEX idx_models_status ON models_3d(status);
CREATE INDEX idx_cv_analysis_project ON cv_analysis(project_id);
CREATE INDEX idx_cv_analysis_type ON cv_analysis(analysis_type);
CREATE INDEX idx_progress_project ON progress_logs(project_id);
CREATE INDEX idx_progress_date ON progress_logs(log_date);
CREATE INDEX idx_chat_conversations_user ON chat_conversations(user_id);
CREATE INDEX idx_chat_messages_conversation ON chat_messages(conversation_id);
CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_read ON notifications(is_read);
CREATE INDEX idx_safety_project ON safety_incidents(project_id);
CREATE INDEX idx_safety_status ON safety_incidents(status);

-- Vector similarity index
CREATE INDEX ON document_embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Updated timestamp triggers
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_boq_items_updated_at BEFORE UPDATE ON boq_items FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_cost_rules_updated_at BEFORE UPDATE ON cost_rules FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_chat_conversations_updated_at BEFORE UPDATE ON chat_conversations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Sample data for development
INSERT INTO users (email, hashed_password, full_name, role) VALUES
('admin@constructai.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewbdktgSeEQDPqV6', 'System Administrator', 'admin'),
('manager@constructai.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewbdktgSeEQDPqV6', 'Project Manager', 'manager'),
('engineer@constructai.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewbdktgSeEQDPqV6', 'Site Engineer', 'engineer');
-- Password for all sample users: 'password123'

INSERT INTO cost_rules (rule_name, category, region, formula, base_rates, labor_rates, overhead_percentage, profit_percentage) VALUES
('Standard Construction', 'general', 'default', 'quantity * unit_rate * (1 + overhead_percentage/100) * (1 + profit_percentage/100)', 
 '{"concrete": 150, "steel": 80, "brick": 25}', '{"mason": 500, "helper": 300, "skilled": 600}', 15.0, 10.0),
('Premium Construction', 'premium', 'default', 'quantity * unit_rate * (1 + overhead_percentage/100) * (1 + profit_percentage/100)', 
 '{"concrete": 200, "steel": 100, "brick": 35}', '{"mason": 700, "helper": 400, "skilled": 800}', 20.0, 15.0);

-- Create sample project
INSERT INTO projects (name, description, owner_id, status, budget, start_date, end_date, location) 
SELECT 
    'Sample Construction Project',
    'A demo project for ConstructAI showcase',
    id,
    'active',
    5000000.00,
    CURRENT_DATE,
    CURRENT_DATE + INTERVAL '6 months',
    '{"address": "123 Construction Ave, Builder City", "coordinates": {"lat": 40.7128, "lng": -74.0060}}'
FROM users WHERE email = 'manager@constructai.com';

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO admin;
