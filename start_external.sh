#!/bin/bash

echo "========================================"
echo "Quantum Chat App - External Access Setup"
echo "========================================"
echo
echo "This script will:"
echo "1. Start the backend server"
echo "2. Start the frontend development server"
echo "3. Give you options for external access"
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
echo "========================================"
echo "Both servers are starting..."
echo "========================================"
echo
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo

echo "Finding your local network IP address..."
LOCAL_IP=$(hostname -I | awk '{print $1}')

echo
echo "========================================"
echo "ACCESS INFORMATION"
echo "========================================"
echo
echo "Local access:        http://localhost:5173"
echo "Local network:       http://$LOCAL_IP:5173"
echo
echo "========================================"
echo "External access options:"
echo "========================================"
echo
echo "1. Set up ngrok tunnel (easiest)"
echo "2. Manual router port forwarding (see PORT_FORWARDING.md)"
echo

read -p "Select an option (1/2 or Ctrl+C to skip): " choice

case $choice in
  1)
    echo
    echo "Starting ngrok tunnel..."
    xterm -e "./tunnel.sh" &
    ;;
  2)
    echo
    echo "Please follow the instructions in PORT_FORWARDING.md"
    echo "to set up router port forwarding."
    echo
    echo "Your internal IP address is: $LOCAL_IP"
    echo
    xdg-open PORT_FORWARDING.md
    ;;
  *)
    echo "No option selected"
    ;;
esac

echo
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo
echo "Press Ctrl+C to stop the servers"

# Handle termination
trap 'kill $BACKEND_PID $FRONTEND_PID; exit' INT TERM

# Wait for child processes
wait
