#!/bin/bash

echo "========================================"
echo "Setting up Quantum Chat Application"
echo "========================================"
echo

# Check if python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install it first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Pip is not installed. Installing pip..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
fi

# Check if nodejs is installed
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed. Installing Node.js and npm..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

echo "Setting up backend..."
cd backend

# Create a Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install backend dependencies
pip install -e .

cd ..

echo "Setting up frontend..."
cd frontend

# Install frontend dependencies
npm install

cd ..

echo "Making scripts executable..."
chmod +x *.sh

echo
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo
echo "To start the application, run:"
echo "  ./start.sh"
echo
echo "For external access options, run:"
echo "  ./start_external.sh"
echo
echo "For development tunnel options, run:"
echo "  ./dev_tunnel.sh"
