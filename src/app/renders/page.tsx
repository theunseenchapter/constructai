'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Camera, Download, Eye, RefreshCw, FolderOpen } from 'lucide-react';
import SafeImage from '@/components/SafeImage';

interface RenderFile {
  name: string;
  path: string;
  publicPath: string;
  size: number;
  created: string;
  url: string;
}

export default function RenderViewerPage() {
  const [renders, setRenders] = useState<RenderFile[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedRender, setSelectedRender] = useState<RenderFile | null>(null);

  const loadRenders = async () => {
    setLoading(true);
    try {
      // First copy files to public directory
      await fetch('/api/renders/copy', { method: 'POST' });
      
      // Then get the list of copied files
      const response = await fetch('/api/renders/copy', { method: 'POST' });
      const data = await response.json();
      setRenders(data.renders || []);
      if (data.renders?.length > 0 && !selectedRender) {
        setSelectedRender(data.renders[0]);
      }
    } catch (error) {
      console.error('Failed to load renders:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRenders();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const formatFileSize = (bytes: number) => {
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    if (bytes === 0) return '0 Bytes';
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
  };

  const downloadRender = (render: RenderFile) => {
    const link = document.createElement('a');
    link.href = render.url;
    link.download = render.name;
    link.click();
  };

  const openInNewTab = (render: RenderFile) => {
    window.open(render.url, '_blank');
  };

  const openTempFolder = () => {
    // This will only work in development or with appropriate permissions
    const tempPath = 'C:\\Users\\' + (process.env.USERNAME || 'Default') + '\\AppData\\Local\\Temp';
    window.open(`file:///${tempPath}`, '_blank');
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            🎨 Blender Render Gallery
          </h1>
          <p className="text-gray-600">
            View and download your generated 3D architectural renders
          </p>
        </div>

        {/* Controls */}
        <div className="flex items-center gap-4 mb-6">
          <Button onClick={loadRenders} disabled={loading} variant="outline">
            <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
          <Button onClick={openTempFolder} variant="outline">
            <FolderOpen className="w-4 h-4 mr-2" />
            Open Temp Folder
          </Button>
          <Badge variant="outline" className="text-sm">
            {renders.length} renders found
          </Badge>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Render List */}
          <Card className="lg:col-span-1">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Camera className="w-5 h-5" />
                Recent Renders
              </CardTitle>
              <CardDescription>
                Click a render to view it
              </CardDescription>
            </CardHeader>
            <CardContent>
              {renders.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  <Camera className="w-12 h-12 mx-auto mb-4 opacity-30" />
                  <p>No renders found</p>
                  <p className="text-sm">Create some renders in the demo first</p>
                </div>
              ) : (
                <div className="space-y-2 max-h-96 overflow-y-auto">
                  {renders.map((render, index) => (
                    <div
                      key={index}
                      className={`p-3 border rounded-lg cursor-pointer transition-all ${
                        selectedRender?.path === render.path
                          ? 'border-blue-500 bg-blue-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                      onClick={() => setSelectedRender(render)}
                    >
                      <div className="font-medium text-sm truncate">
                        {render.name}
                      </div>
                      <div className="text-xs text-gray-500 mt-1">
                        {formatFileSize(render.size)} • {new Date(render.created).toLocaleString()}
                      </div>
                      <div className="flex gap-2 mt-2">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={(e) => {
                            e.stopPropagation();
                            downloadRender(render);
                          }}
                          className="text-xs px-2 py-1 h-6"
                        >
                          <Download className="w-3 h-3 mr-1" />
                          Download
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={(e) => {
                            e.stopPropagation();
                            openInNewTab(render);
                          }}
                          className="text-xs px-2 py-1 h-6"
                        >
                          <Eye className="w-3 h-3 mr-1" />
                          View
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Main Viewer */}
          <Card className="lg:col-span-2">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Eye className="w-5 h-5" />
                Render Preview
              </CardTitle>
              {selectedRender && (
                <CardDescription>
                  {selectedRender.name} • {formatFileSize(selectedRender.size)} • 
                  {new Date(selectedRender.created).toLocaleString()}
                </CardDescription>
              )}
            </CardHeader>
            <CardContent>
              {selectedRender ? (
                <div className="space-y-4">
                  {/* Image */}
                  <div className="border rounded-lg p-4 bg-gray-50">
                    <div className="relative">
                      <SafeImage
                        src={selectedRender.url}
                        alt={selectedRender.name}
                        width={800}
                        height={600}
                        className="max-w-full max-h-full object-contain mx-auto rounded-lg shadow-md"
                      />
                      
                      {/* Overlay Controls */}
                      <div className="absolute top-2 right-2 flex gap-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => downloadRender(selectedRender)}
                          className="bg-white/90 backdrop-blur-sm"
                        >
                          <Download className="w-4 h-4 mr-2" />
                          Download
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => openInNewTab(selectedRender)}
                          className="bg-white/90 backdrop-blur-sm"
                        >
                          <Eye className="w-4 h-4 mr-2" />
                          Full Size
                        </Button>
                      </div>
                    </div>
                  </div>

                  {/* File Info */}
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="font-medium">File Name:</span> {selectedRender.name}
                    </div>
                    <div>
                      <span className="font-medium">File Size:</span> {formatFileSize(selectedRender.size)}
                    </div>
                    <div>
                      <span className="font-medium">Created:</span> {new Date(selectedRender.created).toLocaleString()}
                    </div>
                    <div>
                      <span className="font-medium">Location:</span> Temp Folder
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex gap-4 pt-4 border-t">
                    <Button onClick={() => downloadRender(selectedRender)}>
                      <Download className="w-4 h-4 mr-2" />
                      Download Image
                    </Button>
                    <Button variant="outline" onClick={() => openInNewTab(selectedRender)}>
                      <Eye className="w-4 h-4 mr-2" />
                      View in New Tab
                    </Button>
                    <Button variant="outline" onClick={openTempFolder}>
                      <FolderOpen className="w-4 h-4 mr-2" />
                      Open Folder
                    </Button>
                  </div>
                </div>
              ) : (
                <div className="text-center py-12 text-gray-500">
                  <Camera className="w-12 h-12 mx-auto mb-4 opacity-30" />
                  <p>No render selected</p>
                  <p className="text-sm">Select a render from the list to view it</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Instructions */}
        <Card className="mt-6">
          <CardHeader>
            <CardTitle>📋 How to Access Your Renders</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <h3 className="font-semibold mb-2">💾 Download</h3>
                <p className="text-sm text-gray-600">
                  Click the Download button to save renders to your computer permanently.
                </p>
              </div>
              <div>
                <h3 className="font-semibold mb-2">📁 Temp Folder</h3>
                <p className="text-sm text-gray-600">
                  Renders are temporarily stored in: <br/>
                  <code className="text-xs bg-gray-100 px-1 rounded">
                    C:\Users\{process.env.USERNAME}\AppData\Local\Temp\constructai_blender_*
                  </code>
                </p>
              </div>
              <div>
                <h3 className="font-semibold mb-2">🔄 Auto-Refresh</h3>
                <p className="text-sm text-gray-600">
                  New renders will appear automatically. Click Refresh to update the list manually.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
