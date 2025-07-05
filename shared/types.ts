// Shared TypeScript types for ConstructAI
// Used across frontend, mobile, and backend services

export interface User {
  id: string;
  email: string;
  fullName: string;
  role: 'admin' | 'manager' | 'engineer' | 'worker' | 'user';
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface Project {
  id: string;
  name: string;
  description?: string;
  ownerId: string;
  status: 'planning' | 'active' | 'paused' | 'completed' | 'cancelled';
  budget?: number;
  startDate?: string;
  endDate?: string;
  location?: {
    address: string;
    coordinates: {
      lat: number;
      lng: number;
    };
  };
  createdAt: string;
  updatedAt: string;
}

export interface FileUpload {
  id: string;
  projectId: string;
  filename: string;
  fileType: string;
  fileSize: number;
  minioPath: string;
  uploadBy: string;
  metadata?: Record<string, any>;
  createdAt: string;
}

export interface BOQItem {
  id: string;
  projectId: string;
  itemCode: string;
  description: string;
  unit: string;
  quantity: number;
  unitRate: number;
  totalAmount: number;
  category: string;
  createdAt: string;
}

export interface Model3D {
  id: string;
  projectId: string;
  sourceFileId: string;
  modelPath: string;
  modelType: 'blueprint_conversion' | 'bim' | 'scan';
  conversionParams?: Record<string, any>;
  status: 'processing' | 'completed' | 'failed';
  createdAt: string;
}

export interface CVAnalysis {
  id: string;
  projectId: string;
  sourceFileId: string;
  analysisType: 'ppe_detection' | 'crack_analysis' | 'progress_tracking';
  results: {
    detections?: Array<{
      class: string;
      confidence: number;
      bbox: [number, number, number, number];
    }>;
    cracks?: Array<{
      severity: 'low' | 'medium' | 'high';
      area: number;
      location: [number, number];
    }>;
    progress?: {
      percentage: number;
      completedAreas: string[];
      pendingAreas: string[];
    };
  };
  confidenceScore: number;
  reviewedBy?: string;
  status: 'pending_review' | 'approved' | 'rejected';
  createdAt: string;
}

export interface ProgressLog {
  id: string;
  projectId: string;
  logDate: string;
  progressPercentage: number;
  completionDetails: Record<string, any>;
  photos: string[]; // Array of file IDs
  loggedBy: string;
  notes?: string;
  createdAt: string;
}

export interface ChatConversation {
  id: string;
  userId: string;
  projectId?: string;
  conversationTitle: string;
  language: 'en' | 'hi' | 'es' | 'fr';
  createdAt: string;
}

export interface ChatMessage {
  id: string;
  conversationId: string;
  role: 'user' | 'assistant';
  content: string;
  messageType: 'text' | 'voice' | 'image';
  metadata?: {
    audioUrl?: string;
    imageUrl?: string;
    processingTime?: number;
  };
  createdAt: string;
}

export interface Notification {
  id: string;
  userId: string;
  title: string;
  message: string;
  type: 'info' | 'warning' | 'error' | 'success';
  isRead: boolean;
  actionUrl?: string;
  createdAt: string;
}

// API Response Types
export interface APIResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  hasNext: boolean;
  hasPrev: boolean;
}

// Request Types
export interface CreateProjectRequest {
  name: string;
  description?: string;
  budget?: number;
  startDate?: string;
  endDate?: string;
  location?: {
    address: string;
    coordinates: {
      lat: number;
      lng: number;
    };
  };
}

export interface UpdateProjectRequest extends Partial<CreateProjectRequest> {
  status?: Project['status'];
}

export interface CreateBOQItemRequest {
  itemCode: string;
  description: string;
  unit: string;
  quantity: number;
  unitRate: number;
  category: string;
}

export interface AnalyzeImageRequest {
  fileId: string;
  analysisType: CVAnalysis['analysisType'];
  options?: {
    sensitivity?: number;
    compareWithBIM?: boolean;
    referenceImageId?: string;
  };
}

export interface ChatMessageRequest {
  content: string;
  messageType?: 'text' | 'voice';
  language?: string;
  audioData?: string; // Base64 encoded audio for voice messages
}

// Component Props Types
export interface ProjectCardProps {
  project: Project;
  onEdit?: (project: Project) => void;
  onDelete?: (projectId: string) => void;
  onView?: (projectId: string) => void;
}

export interface FileUploadProps {
  projectId: string;
  acceptedTypes?: string[];
  maxSize?: number;
  onUploadComplete?: (file: FileUpload) => void;
  onUploadError?: (error: string) => void;
}

export interface Model3DViewerProps {
  modelId: string;
  modelPath: string;
  width?: number;
  height?: number;
  showControls?: boolean;
  onLoad?: () => void;
  onError?: (error: string) => void;
}

// State Management Types
export interface AppState {
  user: User | null;
  currentProject: Project | null;
  projects: Project[];
  notifications: Notification[];
  loading: boolean;
  error: string | null;
}

export interface ProjectState {
  files: FileUpload[];
  boqItems: BOQItem[];
  models3D: Model3D[];
  progressLogs: ProgressLog[];
  cvAnalyses: CVAnalysis[];
}

export interface ChatState {
  conversations: ChatConversation[];
  currentConversation: ChatConversation | null;
  messages: ChatMessage[];
  isTyping: boolean;
  isRecording: boolean;
}

// Configuration Types
export interface AppConfig {
  api: {
    baseUrl: string;
    timeout: number;
  };
  storage: {
    minioUrl: string;
    bucketName: string;
  };
  ai: {
    torchServeUrl: string;
    ollamaUrl: string;
    whisperUrl: string;
    ttsUrl: string;
  };
  features: {
    enableVoiceChat: boolean;
    enableOfflineMode: boolean;
    enablePushNotifications: boolean;
  };
}

// Error Types
export interface APIError {
  code: string;
  message: string;
  details?: Record<string, any>;
}

export interface ValidationError {
  field: string;
  message: string;
}

// Utility Types
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

export type Omit<T, K extends keyof T> = Pick<T, Exclude<keyof T, K>>;

export type Status = 'idle' | 'loading' | 'success' | 'error';

// Constants
export const USER_ROLES = ['admin', 'manager', 'engineer', 'worker', 'user'] as const;
export const PROJECT_STATUSES = ['planning', 'active', 'paused', 'completed', 'cancelled'] as const;
export const MESSAGE_TYPES = ['text', 'voice', 'image'] as const;
export const NOTIFICATION_TYPES = ['info', 'warning', 'error', 'success'] as const;
export const CV_ANALYSIS_TYPES = ['ppe_detection', 'crack_analysis', 'progress_tracking'] as const;
export const SUPPORTED_LANGUAGES = ['en', 'hi', 'es', 'fr'] as const;
