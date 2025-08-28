#!/bin/bash

echo "========================================"
echo "Setting up Dev Tunnel for Quantum Chat App"
echo "========================================"
echo
echo "This script will help you set up a dev tunnel for your Quantum Chat app."
echo "A dev tunnel allows external access to your app through a secure URL."
echo
echo "Options:"
echo "1. Use VS Code Dev Tunnels"
echo "2. Use GitHub Codespaces Ports"
echo "3. Use the vscode.dev tunnel"
echo "4. Use other tunneling service"
echo

read -p "Select an option: " choice

case $choice in
  1)
    echo
    echo "To use VS Code Dev Tunnels:"
    echo "1. In VS Code, click on the \"Ports\" tab in the bottom panel"
    echo "2. Click \"Forward a Port\" button"
    echo "3. Enter port 5173 for the frontend"
    echo "4. Right-click on the port and select \"Port Visibility\" → \"Public\""
    echo
    echo "Your app will be accessible at the URL shown in the \"Forwarded Address\" column"
    echo
    read -p "Press Enter to continue..."
    ;;
  2)
    echo
    echo "To use GitHub Codespaces Ports:"
    echo "1. If using Codespaces, open the Ports tab"
    echo "2. Click \"Add Port\" and enter 5173"
    echo "3. Right-click on the port and set visibility to \"Public\""
    echo
    echo "Your app will be accessible at the URL provided by Codespaces"
    echo
    read -p "Press Enter to continue..."
    ;;
  3)
    echo
    echo "To use vscode.dev tunnel:"
    echo "1. In VS Code, go to the Command Palette (Ctrl+Shift+P)"
    echo "2. Type and select \"Dev Tunnels: Create Tunnel\""
    echo "3. Configure the tunnel to forward port 5173"
    echo
    echo "Your app will be accessible at the URL shown after the tunnel is created"
    echo
    read -p "Press Enter to continue..."
    ;;
  4)
    echo
    echo "If using another tunneling service (like cloudflared, localtunnel, etc.):"
    echo
    echo "For cloudflared:"
    echo "  cloudflared tunnel --url http://localhost:5173"
    echo
    echo "For localtunnel:"
    echo "  npx localtunnel --port 5173"
    echo
    echo "Remember: The Vite dev server must be running on port 5173"
    echo "and the backend on port 8000"
    echo
    read -p "Press Enter to continue..."
    ;;
  *)
    echo "Invalid option selected"
    ;;
esac

echo
echo "========================================"
echo "Important Notes for Dev Tunnels:"
echo "========================================"
echo
echo "1. Make sure both frontend and backend servers are running"
echo "2. The frontend server must be running on port 5173"
echo "3. You might need to refresh your browser after connecting"
echo "4. If using VS Code Live Share, others will need to install "
echo "   the Live Share extension and join your session"
echo
echo "========================================"
echo
echo "Starting the servers now..."
echo

echo "Starting backend server..."
cd backend && python -m app.main &
BACKEND_PID=$!

echo "Waiting for backend to start..."
sleep 3

echo "Starting frontend development server..."
cd frontend && npm run dev &
FRONTEND_PID=$!

echo
echo "Servers are starting! Now set up your tunnel using the instructions above."
echo
echo "Press Ctrl+C to stop the servers"

# Handle termination
trap 'kill $BACKEND_PID $FRONTEND_PID; exit' INT TERM

# Wait for child processes
wait
