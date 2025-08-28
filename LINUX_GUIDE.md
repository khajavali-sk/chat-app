# Linux Usage Guide for Quantum Chat App

This guide provides specific instructions for running the Quantum Chat application on Linux/Ubuntu systems.

## Prerequisites

Make sure you have the following installed:

- Python 3.9 or higher
- pip3
- Node.js 16 or higher
- npm

## Quick Setup

1. **Make all scripts executable**:

   ```bash
   chmod +x *.sh
   ```

2. **Run the setup script** (one-time only):
   ```bash
   ./setup.sh
   ```
   This will install all necessary dependencies for both frontend and backend.

## Starting the Application

To start the application with default settings:

```bash
./start.sh
```

This will:

- Start the backend server on port 8000
- Start the frontend server on port 5173
- Make the application accessible at http://localhost:5173

## External Access Options

### Option 1: Access within Local Network

To make the app accessible to other devices on your local network:

```bash
./start_external.sh
```

This will display your local IP address that other devices on the same network can use to access the app.

### Option 2: Access via Development Tunnels

For development and testing with VS Code or GitHub Codespaces tunnels:

```bash
./dev_tunnel.sh
```

Follow the on-screen instructions to set up your preferred tunneling option.

### Option 3: Access via ngrok

For quick public access via ngrok tunneling:

```bash
./tunnel.sh
```

This requires ngrok to be installed. If not installed, you can install it on Ubuntu with:

```bash
sudo snap install ngrok
```

## Stopping the Application

To stop any running servers, press `Ctrl+C` in the terminal window where the servers are running.

## Troubleshooting

### Port Already in Use

If you get an error that ports are already in use, find and kill the processes:

```bash
# Find processes using port 5173 (frontend)
sudo lsof -i :5173

# Find processes using port 8000 (backend)
sudo lsof -i :8000

# Kill a process by PID
kill -9 <PID>
```

### Permission Issues

If you encounter permission issues with the scripts, ensure they're executable:

```bash
chmod +x *.sh
```

### Python Virtual Environment

If you prefer to use a virtual environment manually:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -e .
python -m app.main
```

## Development Notes

- All scripts use relative paths and should be run from the project's root directory
- Frontend development server runs with hot reloading enabled
- Backend also has auto-reload enabled for code changes
