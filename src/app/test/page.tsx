'use client'

import { useEffect, useState } from 'react'

export default function TestPage() {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return (
      <div className="min-h-screen bg-blue-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900">Loading...</h1>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">ConstructAI Test Page</h1>
        <div className="bg-white p-6 rounded-lg shadow-lg">
          <h2 className="text-2xl font-semibold text-blue-600 mb-4">Hydration Test</h2>
          <p className="text-gray-700">
            If you can see this styled content without hydration errors, the frontend is working correctly!
          </p>
          <div className="mt-4 p-4 bg-green-100 rounded border border-green-300">
            <p className="text-green-800 font-medium">✅ Frontend is working properly!</p>
          </div>
        </div>
      </div>
    </div>
  )
}
