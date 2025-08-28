#!/bin/bash

echo "========================================"
echo "Starting Quantum Chat Application"
echo "========================================"
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
echo "Press Ctrl+C to stop the servers"

# Handle termination
trap 'kill $BACKEND_PID $FRONTEND_PID; exit' INT TERM

# Wait for child processes
wait
