# PowerShell script to start ConstructAI backend using conda environment
# This script uses the existing conda environment where packages are installed

Write-Host "🏗️ Starting ConstructAI Backend with Conda Environment..." -ForegroundColor Green
Write-Host "=======================================================" -ForegroundColor Green

# Check if conda is available
try {
    $condaVersion = conda --version 2>&1
    Write-Host "✅ Conda found: $condaVersion" -ForegroundColor Blue
} catch {
    Write-Host "❌ Conda not found. Please install Anaconda or Miniconda." -ForegroundColor Red
    exit 1
}

# Check if we're in the backend directory
if (-not (Test-Path "main.py")) {
    Write-Host "❌ Please run this script from the backend directory" -ForegroundColor Red
    exit 1
}

# Check if constructai environment exists
Write-Host "🔍 Checking for constructai conda environment..." -ForegroundColor Yellow
$envExists = conda env list | Select-String "constructai"
if (-not $envExists) {
    Write-Host "❌ Conda environment 'constructai' not found." -ForegroundColor Red
    Write-Host "Please create it with: conda create -n constructai python=3.11" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Found constructai conda environment" -ForegroundColor Green

# Activate conda environment and check packages
Write-Host "🔄 Activating conda environment..." -ForegroundColor Yellow
conda activate constructai

# Verify key packages are installed
Write-Host "🔍 Verifying required packages..." -ForegroundColor Yellow

$packages = @("fastapi", "uvicorn", "sqlalchemy", "torch", "opencv-python", "pillow", "numpy")
$missing = @()

foreach ($package in $packages) {
    $result = python -c "import $package; print('✅ $package installed')" 2>&1
    if ($LASTEXITCODE -ne 0) {
        $missing += $package
        Write-Host "❌ $package not found" -ForegroundColor Red
    } else {
        Write-Host $result -ForegroundColor Green
    }
}

if ($missing.Count -gt 0) {
    Write-Host "❌ Missing packages: $($missing -join ', ')" -ForegroundColor Red
    Write-Host "Installing missing packages..." -ForegroundColor Yellow
    foreach ($package in $missing) {
        conda install -y $package
    }
}

# Set Python path for development
$env:PYTHONPATH = "$(Get-Location);$env:PYTHONPATH"

# Start the backend server
Write-Host ""
Write-Host "🚀 Starting ConstructAI Backend Server..." -ForegroundColor Green
Write-Host "Server will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Documentation at: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Run with conda environment
python main.py
