// API client for ConstructAI Backend
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ConstructAIClient {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error(`API request failed: ${url}`, error);
      throw error;
    }
  }

  // Health check
  async health() {
    return this.request('/health');
  }

  // Auth endpoints
  async login(username: string, password: string) {
    return this.request('/api/v1/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
  }

  async register(userData: {
    username: string;
    email: string;
    password: string;
    full_name?: string;
  }) {
    return this.request('/api/v1/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  // Projects endpoints
  async getProjects() {
    return this.request('/api/v1/projects/');
  }

  async createProject(projectData: {
    name: string;
    description?: string;
    location?: string;
  }) {
    return this.request('/api/v1/projects/', {
      method: 'POST',
      body: JSON.stringify(projectData),
    });
  }

  async getProject(projectId: number) {
    return this.request(`/api/v1/projects/${projectId}`);
  }

  // Files endpoints
  async uploadFile(file: File, projectId?: number) {
    const formData = new FormData();
    formData.append('file', file);
    if (projectId) {
      formData.append('project_id', projectId.toString());
    }

    return this.request('/api/v1/files/upload', {
      method: 'POST',
      body: formData,
      headers: {}, // Remove Content-Type to let browser set it for FormData
    });
  }

  async getFiles(projectId?: number) {
    const params = projectId ? `?project_id=${projectId}` : '';
    return this.request(`/api/v1/files/${params}`);
  }

  // Real AI file processing endpoints
  private async processFile(
    endpoint: string,
    file: File,
    additionalData?: Record<string, string | number>
  ): Promise<unknown> {
    const formData = new FormData();
    formData.append('file', file);
    
    if (additionalData) {
      Object.entries(additionalData).forEach(([key, value]) => {
        formData.append(key, String(value));
      });
    }

    const url = `${this.baseURL}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
          // Add cache-busting headers
          'Cache-Control': 'no-cache, no-store, must-revalidate',
          'Pragma': 'no-cache',
          'Expires': '0'
        },
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error(`File processing failed: ${url}`, error);
      throw error;
    }
  }

  // 2D to 3D conversion with real image processing
  async convert2DTo3D(file: File) {
    // Add timestamp to prevent caching
    const timestamp = Date.now();
    const endpoint = `/api/v1/ai/convert-2d-to-3d?t=${timestamp}`;
    return this.processFile(endpoint, file);
  }

  // PPE detection with real computer vision
  async detectPPE(file: File) {
    return this.processFile('/api/v1/ai/vision/analyze', file);
  }

  // Crack detection (using the same vision analysis endpoint)
  async detectCracks(file: File) {
    return this.processFile('/api/v1/ai/vision/analyze', file);
  }

  // Progress tracking (using the same vision analysis endpoint)
  async trackProgress(file: File) {
    return this.processFile('/api/v1/ai/vision/analyze', file);
  }

  // Real BOQ calculation with specifications
  async calculateDetailedBOQ(specs: {
    total_area: number;
    num_rooms: number;
    num_bathrooms: number;
    num_floors?: number;
    construction_type?: string;
    quality_grade?: string;
    location?: string;
  }) {
    return this.request('/api/v1/boq/estimate', {
      method: 'POST',
      body: JSON.stringify(specs),
    });
  }

  // Quick cost estimation
  async quickEstimate(area_sqft: number, construction_type: string = 'residential') {
    return this.request(`/api/v1/boq/quick-estimate?area_sqft=${area_sqft}&construction_type=${construction_type}`, {
      method: 'POST',
    });
  }

  // Chat with real AI
  async askRealChatbot(message: string, language: string = 'en') {
    return this.request('/api/v1/chat/ask', {
      method: 'POST',
      body: JSON.stringify({ message, language }),
    });
  }

  // Get AI models status
  async getModelsStatus() {
    return this.request('/api/v1/ai/models/status');
  }

  // Safety endpoints
  async detectPPEOnSite(file: File) {
    const formData = new FormData();
    formData.append('file', file);

    return this.request('/api/v1/safety/ppe-detection', {
      method: 'POST',
      body: formData,
      headers: {},
    });
  }

  async getSafetyReports() {
    return this.request('/api/v1/safety/reports');
  }

  // BOQ endpoints (legacy for backward compatibility)
  async calculateBOQ() {
    return this.request('/api/v1/boq/estimate', {
      method: 'POST',
    });
  }

  async getBOQ(boqId: string) {
    return this.request(`/api/v1/boq/${boqId}`);
  }

  async exportBOQ(boqId: string, format: 'pdf' | 'xlsx' = 'pdf') {
    return this.request(`/api/v1/boq/export/${boqId}?format=${format}`, {
      method: 'POST',
    });
  }

  // Chat endpoints (legacy for backward compatibility)
  async askChatbot(message: string, language: string = 'en') {
    return this.askRealChatbot(message, language);
  }

  async getChatHistory() {
    return this.request('/api/v1/chat/history');
  }

  async getSupportedLanguages() {
    return this.request('/api/v1/chat/languages');
  }
}

// Create a singleton instance
export const constructAI = new ConstructAIClient();

// Export types for TypeScript
export interface Project {
  id: number;
  name: string;
  description?: string;
  location?: string;
  created_at: string;
  updated_at: string;
}

export interface FileInfo {
  id: number;
  filename: string;
  original_filename: string;
  file_size: number;
  content_type: string;
  upload_date: string;
  project_id?: number;
}

export interface APIResponse {
  message: string;
  data?: Record<string, unknown>;
}

export default ConstructAIClient;
