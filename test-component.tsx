// Test JSX syntax
function TestComponent() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-6" suppressHydrationWarning={true}>
      <div className="max-w-7xl mx-auto" suppressHydrationWarning={true}>
        <div className="mb-8 text-center">
          <h1>Test</h1>
        </div>
      </div>
    </div>
  )
}

export default TestComponent
