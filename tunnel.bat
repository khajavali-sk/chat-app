@echo off
echo ============================================================
echo Setting up ngrok tunnel for Quantum Chat App
echo ============================================================
echo.

:: Check if ngrok is installed
where ngrok >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ngrok is not installed or not in your PATH.
    echo Please install ngrok from https://ngrok.com/download
    echo and add it to your PATH, then run this script again.
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

echo Starting ngrok tunnel for frontend (port 5173)...
echo This will make your app accessible from the internet.
echo.
echo NOTE: The free version of ngrok will give you a random URL
echo that changes each time you restart ngrok.
echo.
echo Press Ctrl+C to stop the tunnel when you're done.
echo.

:: Start ngrok tunnel for the frontend
ngrok http 5173

echo.
echo ============================================================
echo Tunnel stopped.
echo ============================================================
