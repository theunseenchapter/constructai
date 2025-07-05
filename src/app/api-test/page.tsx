'use client';

import { useState, useEffect } from 'react';
import { constructAI } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

// Define types for API responses
interface HealthResponse {
  service: string;
  version: string;
  status: string;
}

interface Project {
  id?: number;
  name: string;
  description: string;
  location: string;
  created_at?: string;
}

interface AIModelStatus {
  status: string;
  model?: string;
}

interface AIStatusResponse {
  data?: {
    [key: string]: AIModelStatus;
  };
}

interface ChatResponse {
  data?: {
    response?: string;
  };
}

export default function APITestPage() {
  const [backendStatus, setBackendStatus] = useState<'connecting' | 'connected' | 'error'>('connecting');
  const [healthData, setHealthData] = useState<HealthResponse | null>(null);
  const [projects, setProjects] = useState<Project[]>([]);
  const [aiStatus, setAiStatus] = useState<AIStatusResponse | null>(null);

  useEffect(() => {
    testBackendConnection();
  }, []);

  const testBackendConnection = async () => {
    try {
      const health = await constructAI.health();
      setHealthData(health as HealthResponse);
      setBackendStatus('connected');
      
      // Test other endpoints
      const projectsData = await constructAI.getProjects();
      setProjects(projectsData as Project[]);
      
      const aiStatusData = await constructAI.getModelsStatus();
      setAiStatus(aiStatusData as AIStatusResponse);
      
    } catch (error) {
      console.error('Backend connection failed:', error);
      setBackendStatus('error');
    }
  };

  const testCreateProject = async () => {
    try {
      const newProject = await constructAI.createProject({
        name: 'Test Project ' + Date.now(),
        description: 'Created from frontend test',
        location: 'Test Location'
      });
      console.log('Created project:', newProject);
      
      // Refresh projects list
      const updatedProjects = await constructAI.getProjects();
      setProjects(updatedProjects as Project[]);
    } catch (error) {
      console.error('Failed to create project:', error);
    }
  };

  const testChatbot = async () => {
    try {
      const response = await constructAI.askChatbot('Hello, can you help me with construction planning?');
      const chatResponse = response as ChatResponse;
      console.log('Chatbot response:', response);
      alert(`Chatbot says: ${chatResponse.data?.response || 'No response'}`);
    } catch (error) {
      console.error('Chatbot test failed:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">🧪 ConstructAI API Test Page</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          
          {/* Backend Connection Status */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                {backendStatus === 'connected' && '✅'}
                {backendStatus === 'connecting' && '🔄'}
                {backendStatus === 'error' && '❌'}
                Backend Status
              </CardTitle>
              <CardDescription>
                Connection to FastAPI backend
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <p><strong>Status:</strong> {backendStatus}</p>
                {healthData && (
                  <>
                    <p><strong>Service:</strong> {healthData.service}</p>
                    <p><strong>Version:</strong> {healthData.version}</p>
                  </>
                )}
                <Button onClick={testBackendConnection} className="w-full">
                  Test Connection
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Projects */}
          <Card>
            <CardHeader>
              <CardTitle>📋 Projects</CardTitle>
              <CardDescription>
                Test project management
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <p><strong>Count:</strong> {projects.length}</p>
                <div className="max-h-32 overflow-y-auto">
                  {projects.map((project, index) => (
                    <div key={index} className="text-sm p-2 bg-blue-50 rounded">
                      <strong>{project.name}</strong>
                      <br />
                      <span className="text-gray-600">{project.location}</span>
                    </div>
                  ))}
                </div>
                <Button onClick={testCreateProject} className="w-full">
                  Create Test Project
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* AI Models Status */}
          <Card>
            <CardHeader>
              <CardTitle>🤖 AI Models</CardTitle>
              <CardDescription>
                AI services status
              </CardDescription>
            </CardHeader>
            <CardContent>
              {aiStatus ? (
                <div className="space-y-2">
                  {Object.entries(aiStatus.data || {}).map(([key, value]: [string, AIModelStatus]) => (
                    <div key={key} className="text-sm">
                      <span className="font-medium">{key}:</span>
                      <span className={`ml-2 px-2 py-1 rounded text-xs ${
                        value.status === 'online' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                      }`}>
                        {value.status}
                      </span>
                    </div>
                  ))}
                </div>
              ) : (
                <p>Loading AI status...</p>
              )}
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <Card className="md:col-span-2 lg:col-span-3">
            <CardHeader>
              <CardTitle>⚡ Quick API Tests</CardTitle>
              <CardDescription>
                Test different API endpoints
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <Button onClick={testChatbot} variant="outline">
                  🗣️ Test Chatbot
                </Button>
                <Button onClick={() => constructAI.calculateBOQ().then(console.log)} variant="outline">
                  💰 Test BOQ
                </Button>
                <Button onClick={() => constructAI.getSafetyReports().then(console.log)} variant="outline">
                  🦺 Test Safety
                </Button>
                <Button onClick={() => constructAI.getSupportedLanguages().then(console.log)} variant="outline">
                  🌐 Test Languages
                </Button>
              </div>
            </CardContent>
          </Card>

        </div>

        {/* API Documentation Link */}
        <Card className="mt-6">
          <CardContent className="pt-6">
            <div className="text-center">
              <h3 className="text-lg font-semibold mb-2">📚 Backend API Documentation</h3>
              <p className="text-gray-600 mb-4">
                Explore all available endpoints in the interactive API docs
              </p>
              <Button onClick={() => window.open('http://localhost:8000/docs', '_blank')}>
                Open API Docs (Swagger UI)
              </Button>
            </div>
          </CardContent>
        </Card>

      </div>
    </div>
  );
}
