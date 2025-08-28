@echo off
echo ========================================
echo Quantum Chat App - External Access Setup
echo ========================================
echo.
echo This script will:
echo 1. Start the backend server
echo 2. Start the frontend development server
echo 3. Give you options for external access
echo.

echo Starting backend server...
start "Quantum Chat Backend" cmd /k "cd backend && uv run python main.py"

echo Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo Starting frontend development server...
start "Quantum Chat Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo Both servers are starting...
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.

echo Finding your local network IP address...
for /f "tokens=4" %%a in ('route print ^| find " 0.0.0.0"') do set LOCAL_IP=%%a

echo.
echo ========================================
echo ACCESS INFORMATION
echo ========================================
echo.
echo Local access:        http://localhost:5173
echo Local network:       http://%LOCAL_IP%:5173
echo.
echo ========================================
echo External access options:
echo ========================================
echo.
echo 1. Set up ngrok tunnel (easiest)
echo 2. Manual router port forwarding (see PORT_FORWARDING.md)
echo.

choice /C 12 /M "Select an option (or close this window to skip): "

if errorlevel 2 goto :router_instructions
if errorlevel 1 goto :setup_ngrok

:setup_ngrok
echo.
echo Starting ngrok tunnel...
start "Quantum Chat Tunnel" cmd /k "call tunnel.bat"
goto :end

:router_instructions
echo.
echo Please follow the instructions in PORT_FORWARDING.md
echo to set up router port forwarding.
echo.
echo Your internal IP address is: %LOCAL_IP%
echo.
start "" PORT_FORWARDING.md

:end
echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo Press any key to close this window...
pause >nul
