'use client'

import ClientOnly from "@/components/ClientOnly"
import Dashboard from "@/components/Dashboard"
import ErrorBoundary from "@/components/ErrorBoundary"

export default function Home() {
  return (
    <ErrorBoundary>
      <ClientOnly
        fallback={
          <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
            <div className="text-center">
              <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <h2 className="text-2xl font-bold text-gray-900">Loading ConstructAI...</h2>
              <p className="text-gray-600 mt-2">Initializing AI-powered construction management</p>
            </div>
          </div>
        }
      >
        <Dashboard />
      </ClientOnly>
    </ErrorBoundary>
  )
}
