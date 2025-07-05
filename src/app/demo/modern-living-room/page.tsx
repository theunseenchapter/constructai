/**
 * Modern Living Room Demo Page
 * Showcases 3D scene creation with Blender MCP server
 */

'use client';

import ModernLivingRoomDemo from '@/components/ModernLivingRoomDemo';

export default function ModernLivingRoomPage() {
  const handleSceneCreated = (sceneData: unknown) => {
    console.log('Scene created:', sceneData);
  };

  const handleRenderComplete = (renderData: unknown) => {
    console.log('Render complete:', renderData);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">
            🏠 Modern Living Room Demo
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Experience AI-powered 3D architectural visualization using Blender MCP server 
            integration with GitHub Copilot in VS Code.
          </p>
        </div>

        <ModernLivingRoomDemo
          onSceneCreated={handleSceneCreated}
          onRenderComplete={handleRenderComplete}
        />

        <div className="mt-12 bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-semibold mb-4">🤖 GitHub Copilot Integration</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-medium mb-3">How it works:</h3>
              <ul className="space-y-2 text-gray-600">
                <li>• GitHub Copilot connects to the Blender MCP server</li>
                <li>• MCP protocol handles 3D scene creation requests</li>
                <li>• Blender generates realistic architectural visualization</li>
                <li>• Real-time rendering with customizable views</li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-medium mb-3">Features:</h3>
              <ul className="space-y-2 text-gray-600">
                <li>• Modern furniture placement and lighting</li>
                <li>• Material and texture simulation</li>
                <li>• Single and 360-degree view rendering</li>
                <li>• VS Code integration with GitHub Copilot</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="mt-8 bg-blue-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-800 mb-3">💡 Try with GitHub Copilot:</h3>
          <div className="text-blue-700 space-y-2">
            <p>Ask GitHub Copilot in VS Code:</p>
            <code className="block bg-blue-100 p-2 rounded text-sm">
              &quot;@workspace Create a 3D scene with a modern living room using the Blender MCP server&quot;
            </code>
            <code className="block bg-blue-100 p-2 rounded text-sm">
              &quot;@workspace Render the scene in 360-degree view&quot;
            </code>
          </div>
        </div>
      </div>
    </div>
  );
}
