# PowerShell script to start the Blender MCP Server
Write-Host "Starting Blender MCP Server for ConstructAI..." -ForegroundColor Green

# Set environment variables
$env:BLENDER_PATH = "blender"  # Assume Blender is in PATH, otherwise set full path
$env:PYTHONPATH = "$PWD;$env:PYTHONPATH"

# Check if Python environment is activated
if (-not $env:CONDA_DEFAULT_ENV -and -not $env:VIRTUAL_ENV) {
    Write-Host "Warning: No Python environment detected. Make sure you have activated the constructai environment." -ForegroundColor Yellow
}

# Start the MCP server
Write-Host "Starting MCP server..." -ForegroundColor Cyan
try {
    python start_mcp_server.py
} catch {
    Write-Host "Error starting MCP server: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "MCP server stopped." -ForegroundColor Green
