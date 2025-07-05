@echo off
REM Batch script to start ConstructAI backend using conda environment

echo 🏗️ Starting ConstructAI Backend with Conda Environment...
echo =======================================================

REM Check if we're in the backend directory
if not exist "main.py" (
    echo ❌ Please run this script from the backend directory
    pause
    exit /b 1
)

REM Activate conda environment
echo 🔄 Activating conda environment...
call conda activate constructai

REM Verify key packages
echo 🔍 Verifying required packages...
python -c "import fastapi; print('✅ fastapi installed')" 2>NUL || echo ❌ fastapi not found
python -c "import uvicorn; print('✅ uvicorn installed')" 2>NUL || echo ❌ uvicorn not found
python -c "import sqlalchemy; print('✅ sqlalchemy installed')" 2>NUL || echo ❌ sqlalchemy not found
python -c "import torch; print('✅ torch installed')" 2>NUL || echo ❌ torch not found

REM Set Python path for development
set PYTHONPATH=%cd%;%PYTHONPATH%

REM Start the backend server
echo.
echo 🚀 Starting ConstructAI Backend Server...
echo Server will be available at: http://localhost:8000
echo API Documentation at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run with conda environment
python main.py

pause
