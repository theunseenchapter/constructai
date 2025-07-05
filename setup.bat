@echo off
echo.
echo ===============================================
echo    ConstructAI Blender MCP Setup Script
echo ===============================================
echo.

REM Check if we're in the right directory
if not exist "package.json" (
    echo ❌ Error: package.json not found. Please run this script from the ConstructAI root directory.
    pause
    exit /b 1
)

echo ✅ Found package.json - proceeding with setup...
echo.

REM Check Node.js installation
echo 📦 Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)
echo ✅ Node.js is installed

REM Check Python installation
echo 🐍 Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org/
    pause
    exit /b 1
)
echo ✅ Python is installed

REM Check Blender installation
echo 🎨 Checking Blender installation...
blender --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Blender not found in PATH - you may need to install it
    echo Download from https://www.blender.org/
    echo Script will continue but 3D features may not work
) else (
    echo ✅ Blender is installed
)
echo.

REM Install npm dependencies
echo 📦 Installing npm dependencies...
call npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install npm dependencies
    pause
    exit /b 1
)
echo ✅ npm dependencies installed
echo.

REM Install Python MCP dependencies
echo 🐍 Installing Python MCP dependencies...
pip install mcp anthropic-tools asyncio
if %errorlevel% neq 0 (
    echo ⚠️  Failed to install Python MCP dependencies
    echo You may need to install them manually: pip install mcp anthropic-tools asyncio
)
echo.

REM Build the project
echo 🔨 Building the project...
call npm run build
if %errorlevel% neq 0 (
    echo ❌ Build failed - please check the errors above
    pause
    exit /b 1
)
echo ✅ Project built successfully
echo.

REM Check VS Code configuration
echo 📝 Checking VS Code configuration...
if exist ".vscode\settings.json" (
    echo ✅ VS Code MCP configuration found
) else (
    echo ⚠️  VS Code configuration not found - creating it...
    mkdir .vscode 2>nul
    echo { > .vscode\settings.json
    echo   "mcp.servers": { >> .vscode\settings.json
    echo     "constructai-blender": { >> .vscode\settings.json
    echo       "command": "python", >> .vscode\settings.json
    echo       "args": ["%cd%\backend\start_mcp_server.py"], >> .vscode\settings.json
    echo       "cwd": "%cd%" >> .vscode\settings.json
    echo     } >> .vscode\settings.json
    echo   } >> .vscode\settings.json
    echo } >> .vscode\settings.json
    echo ✅ VS Code configuration created
)
echo.

REM Final setup check
echo 🧪 Running setup verification...
python test_integration.py
echo.

echo ===============================================
echo           Setup Complete! 🎉
echo ===============================================
echo.
echo 📋 Next Steps:
echo.
echo 1. Start the development server:
echo    npm run dev
echo.
echo 2. Open VS Code in this folder:
echo    code .
echo.
echo 3. Try the demos:
echo    - BOQ Calculator: http://localhost:3001/boq
echo    - 3D Demo: http://localhost:3001/demo/modern-living-room
echo.
echo 4. Use GitHub Copilot with commands like:
echo    @constructai-blender Create a modern kitchen
echo.
echo ===============================================
echo.
pause
