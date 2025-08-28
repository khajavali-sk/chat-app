# Quantum Chat - Multi-User Real-Time Secure Chat Application

A demonstration of quantum-secured communication using the BB84 protocol for quantum key distribution (QKD) with real-time chat capabilities.

## 🔬 Overview

This application simulates quantum cryptography concepts to create a secure multi-user chat system. It demonstrates:

- **Quantum Key Distribution (BB84 Protocol)**: Simulated quantum key exchange between users
- **Eavesdropper Detection**: Automatic detection of security breaches during key exchange
- **End-to-End Encryption**: Messages encrypted with quantum-generated session keys
- **Real-Time Communication**: WebSocket-based instant messaging
- **Multi-User Support**: Multiple simultaneous secure chat sessions

## 🏗️ Architecture

### Backend (FastAPI + WebSockets)

- **FastAPI**: High-performance web framework for Python
- **WebSockets**: Real-time bidirectional communication
- **Qiskit**: Quantum computing framework for BB84 simulation
- **Cryptography**: Symmetric encryption using Fernet
- **UV**: Modern Python package management

### Frontend (React + TailwindCSS)

- **React 18**: Modern UI framework with hooks
- **TailwindCSS**: Utility-first CSS framework
- **Lucide React**: Beautiful icon library
- **WebSocket API**: Native browser WebSocket support

### Security Layer

- **BB84 Protocol**: Quantum key distribution simulation
- **Eavesdropper Detection**: Statistical analysis of quantum measurements
- **Symmetric Encryption**: AES-based encryption with quantum-derived keys
- **Session Isolation**: Individual encryption keys per chat session

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+
- UV package manager (install with `pip install uv`)

### Windows Setup

The easiest way to set up the application on Windows is using the provided batch scripts:

```cmd
# Run the setup script (one time only)
setup.bat

# Start the application
start.bat
```

### Linux/Ubuntu Setup

For Linux/Ubuntu users, use the shell scripts:

```bash
# Make scripts executable
chmod +x *.sh

# Run the setup script (one time only)
./setup.sh

# Start the application
./start.sh
```

### Backend Setup (Manual)

```bash
# Navigate to backend directory
cd backend

# Install dependencies
uv pip install -e .

# Start the server
python -m app.main
```

### Frontend Setup (Manual)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The application will start with backend on `http://localhost:8000` and frontend on `http://localhost:5173`

### External Access Options

#### Windows

```cmd
# For general external access options
start_external.bat

# For development tunnels (VS Code, GitHub Codespaces, etc.)
dev_tunnel.bat

# For ngrok tunneling
tunnel.bat
```

#### Linux/Ubuntu

```bash
# For general external access options
./start_external.sh

# For development tunnels (VS Code, GitHub Codespaces, etc.)
./dev_tunnel.sh

# For ngrok tunneling
./tunnel.sh
```

See `PORT_FORWARDING.md` for detailed instructions on various external access methods.

## 📱 Usage

### 1. Join the Network

- Open the application in your browser
- Enter a display name and unique user ID
- Click "Connect to Quantum Network"

### 2. Initiate Secure Chat

- See other online users in the user list
- Click "Secure Chat" next to any user
- This starts the quantum key distribution process

### 3. QKD Handshake

- The system performs BB84 quantum key exchange
- Both users must accept the QKD request
- If an eavesdropper is detected, the connection is terminated
- If successful, a secure channel is established

### 4. Secure Communication

- Send encrypted messages in real-time
- All messages are encrypted with quantum-generated keys
- View key fingerprint for verification
- End session when finished

## 🔐 Security Features

### Quantum Key Distribution (BB84)

```
Alice prepares qubits → Quantum Channel → Bob measures qubits
     ↓                                           ↓
Random bits & bases                    Random measurement bases
     ↓                                           ↓
Public discussion of bases → Sifted Key → Error checking
     ↓                                           ↓
Eavesdropper detection ← Error rate analysis ← Final key
```

### Eavesdropper Detection

- Statistical analysis of measurement errors
- Threshold-based detection (>11% error rate)
- Automatic connection termination on detection
- Security alerts for users

### Encryption

- Quantum-derived 256-bit symmetric keys
- Fernet encryption (AES 128 in CBC mode)
- HMAC authentication
- Perfect forward secrecy

## 🧪 Testing QKD

Test the quantum key distribution independently:

```bash
cd backend
uv run python -m app.security.qkd
```

This demonstrates:

- Normal key generation (no eavesdropper)
- Eavesdropper detection scenarios
- Error rate analysis

## 🌐 API Endpoints

### WebSocket

- `ws://localhost:8000/ws/{user_id}?display_name={name}` - Main chat WebSocket

### HTTP

- `GET /` - Health check
- `GET /api/health` - Detailed system status
- `POST /api/decrypt-message` - Decrypt message for display
- `POST /api/upload-file` - Upload encrypted files

## 📁 Project Structure

```
chat-app/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   └── security/
│   │       ├── qkd.py           # BB84 protocol implementation
│   │       └── encryption.py    # Encryption utilities
│   ├── pyproject.toml           # Python dependencies
│   └── main.py                  # Application entry point
│
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── hooks/               # Custom hooks
│   │   ├── App.js               # Main application
│   │   └── index.js             # Application entry point
│   ├── package.json             # Node.js dependencies
│   └── tailwind.config.js       # TailwindCSS configuration
│
└── README.md                    # This file
```

## 🔬 How It Works

### 1. User Connection

- Users connect via WebSocket with unique IDs
- Server maintains active connections and user list
- Real-time updates of online users

### 2. QKD Initiation

- User A requests secure chat with User B
- Server creates pending QKD session
- User B receives request notification

### 3. BB84 Protocol Execution

```python
# Simplified BB84 implementation
def run_bb84_protocol():
    # Alice generates random bits and bases
    alice_bits = random_bits(n)
    alice_bases = random_bases(n)

    # Alice prepares qubits
    qubits = prepare_qubits(alice_bits, alice_bases)

    # Optional: Eve intercepts (eavesdropping simulation)
    if eavesdropper:
        qubits = eve_intercept(qubits)

    # Bob measures with random bases
    bob_bases = random_bases(n)
    bob_results = measure_qubits(qubits, bob_bases)

    # Public basis comparison and key sifting
    sifted_key = sift_key(alice_bits, alice_bases, bob_bases, bob_results)

    # Eavesdropper detection
    if detect_eavesdropping(sifted_key):
        return None, True

    # Privacy amplification
    final_key = hash_key(sifted_key)
    return final_key, False
```

### 4. Secure Communication

- Successful QKD creates shared symmetric key
- All messages encrypted with session key
- Real-time encrypted message exchange
- Automatic decryption for display

## ⚠️ Security Considerations

### This is a Demonstration

- **Educational Purpose**: Illustrates quantum cryptography concepts
- **Simulation Only**: Real QKD requires quantum hardware
- **No Physical Security**: Uses classical communication channels
- **Simplified Implementation**: Production systems need additional security layers

### Real-World QKD Requirements

- Quantum hardware (photon sources, detectors)
- Authenticated classical channels
- Physical security of quantum channels
- Advanced error correction
- Key management infrastructure

## 🛠️ Development

### Adding Features

- File sharing with encryption
- Group chat capabilities
- Message persistence
- Advanced authentication
- Rate limiting and abuse prevention

### Testing

```bash
# Backend tests
cd backend
uv run pytest

# Frontend tests
cd frontend
npm test
```

### Environment Variables

```bash
# backend/.env
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 📚 References

- [BB84 Protocol](https://en.wikipedia.org/wiki/BB84) - Original quantum key distribution protocol
- [Qiskit Documentation](https://qiskit.org/documentation/) - Quantum computing framework
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React Documentation](https://reactjs.org/docs/) - UI framework documentation

## 📄 License

This project is for educational purposes and demonstrates quantum cryptography concepts. Not intended for production security applications.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🔮 Future Enhancements

- [ ] Integration with real quantum hardware
- [ ] Advanced error correction protocols
- [ ] Multiple QKD protocol support (E91, SARG04)
- [ ] Quantum digital signatures
- [ ] Mobile application support
- [ ] Group chat with multiparty QKD
