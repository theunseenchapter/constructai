'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

interface FileInfo {
  name: string
  size: number
  modified: string
  type: 'obj' | 'ply' | 'other'
}

export default function FileBrowserPage() {
  const [files, setFiles] = useState<FileInfo[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchFiles()
  }, [])

  const fetchFiles = async () => {
    try {
      setLoading(true)
      const response = await fetch('/api/files/list')
      if (!response.ok) {
        throw new Error(`Failed to fetch files: ${response.status}`)
      }
      const data = await response.json()
      setFiles(data.files || [])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load files')
    } finally {
      setLoading(false)
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  const getFileIcon = (type: string) => {
    switch (type) {
      case 'obj': return '📦'
      case 'ply': return '🔷'
      default: return '📄'
    }
  }

  const isNerfFile = (name: string) => name.startsWith('nerf_')

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading files...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Error Loading Files</h1>
          <p className="text-gray-600 mb-4">{error}</p>
          <button 
            onClick={fetchFiles}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Try Again
          </button>
        </div>
      </div>
    )
  }

  const nerfFiles = files.filter(f => isNerfFile(f.name))
  const otherFiles = files.filter(f => !isNerfFile(f.name))

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto py-8 px-4">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            📁 Generated 3D Models
          </h1>
          <p className="text-gray-600">
            Browse and download all available 3D model files. NeRF models are generated from images.
          </p>
          
          <div className="mt-4 flex gap-4">
            <Link href="/" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
              ← Back to Home
            </Link>
            <Link href="/test-living-room.html" className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
              🧪 Generate New NeRF
            </Link>
            <button 
              onClick={fetchFiles}
              className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
            >
              🔄 Refresh
            </button>
          </div>
        </div>

        {/* Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-2xl font-bold text-blue-600">{files.length}</div>
            <div className="text-gray-600">Total Files</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-2xl font-bold text-green-600">{nerfFiles.length}</div>
            <div className="text-gray-600">NeRF Models</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-2xl font-bold text-purple-600">
              {formatFileSize(files.reduce((sum, f) => sum + f.size, 0))}
            </div>
            <div className="text-gray-600">Total Size</div>
          </div>
        </div>

        {/* NeRF Files Section */}
        {nerfFiles.length > 0 && (
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              🧠 NeRF Models ({nerfFiles.length})
            </h2>
            <div className="bg-white rounded-lg shadow overflow-hidden">
              <div className="overflow-x-auto">
                <table className="min-w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">File</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Size</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Modified</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {nerfFiles.map((file) => (
                      <tr key={file.name} className="hover:bg-gray-50">
                        <td className="px-6 py-4">
                          <div className="flex items-center">
                            <span className="text-2xl mr-3">{getFileIcon(file.type)}</span>
                            <span className="font-medium text-gray-900">{file.name}</span>
                          </div>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-600 uppercase">
                          {file.type}
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-600">
                          {formatFileSize(file.size)}
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-600">
                          {new Date(file.modified).toLocaleString()}
                        </td>
                        <td className="px-6 py-4">
                          <a 
                            href={`/api/download/${file.name}`}
                            className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700"
                            download
                          >
                            📥 Download
                          </a>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* Other Files Section */}
        {otherFiles.length > 0 && (
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              📄 Other Files ({otherFiles.length})
            </h2>
            <div className="bg-white rounded-lg shadow overflow-hidden">
              <div className="overflow-x-auto">
                <table className="min-w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">File</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Size</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Modified</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {otherFiles.map((file) => (
                      <tr key={file.name} className="hover:bg-gray-50">
                        <td className="px-6 py-4">
                          <div className="flex items-center">
                            <span className="text-2xl mr-3">{getFileIcon(file.type)}</span>
                            <span className="font-medium text-gray-900">{file.name}</span>
                          </div>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-600 uppercase">
                          {file.type}
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-600">
                          {formatFileSize(file.size)}
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-600">
                          {new Date(file.modified).toLocaleString()}
                        </td>
                        <td className="px-6 py-4">
                          <a 
                            href={`/api/download/${file.name}`}
                            className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700"
                            download
                          >
                            📥 Download
                          </a>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {files.length === 0 && (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">📭</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">No Files Found</h2>
            <p className="text-gray-600 mb-6">
              No 3D models have been generated yet. Create your first NeRF model from images.
            </p>
            <Link 
              href="/test-living-room.html"
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
            >
              🧪 Generate NeRF Model
            </Link>
          </div>
        )}
      </div>
    </div>
  )
}
