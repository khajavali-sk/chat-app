"""
Main FastAPI application for quantum-secured chat
"""

from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
    HTTPException,
    UploadFile,
    File,
    Form,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json
import asyncio
import uuid
from datetime import datetime
from typing import Dict, List, Set, Optional
import base64
import os
from PIL import Image
import io

from .security.qkd import generate_session_key
from .security.encryption import encryption_manager, create_session_key_hash


app = FastAPI(title="Quantum Chat API", version="1.0.0")

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:*",  # Allow any port on localhost
        "*",  # Allow all origins for development/testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConnectionManager:
    """Manages WebSocket connections and user sessions"""

    def __init__(self):
        # Active WebSocket connections: user_id -> websocket
        self.active_connections: Dict[str, WebSocket] = {}
        # User information: user_id -> user_info
        self.users: Dict[str, dict] = {}
        # Active chat sessions: session_id -> {user1, user2, established}
        self.chat_sessions: Dict[str, dict] = {}
        # Pending QKD handshakes: session_id -> {initiator, target, status}
        self.pending_qkd: Dict[str, dict] = {}

    async def connect(self, websocket: WebSocket, user_id: str, display_name: str):
        """Connect a new user"""
        await websocket.accept()
        self.active_connections[user_id] = websocket
        self.users[user_id] = {
            "id": user_id,
            "display_name": display_name,
            "connected_at": datetime.now().isoformat(),
            "status": "online",
        }

        # Notify all users about the new connection
        await self.broadcast_user_list()

        # Send welcome message
        await self.send_personal_message(
            {
                "type": "welcome",
                "message": "Connected to Quantum Chat",
                "user_id": user_id,
            },
            user_id,
        )

    async def disconnect(self, user_id: str):
        """Disconnect a user and cleanup"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]

        if user_id in self.users:
            del self.users[user_id]

        # Clean up any pending QKD sessions
        sessions_to_remove = []
        for session_id, session_info in list(self.pending_qkd.items()):
            if user_id in [session_info.get("initiator"), session_info.get("target")]:
                sessions_to_remove.append(session_id)

        for session_id in sessions_to_remove:
            if session_id in self.pending_qkd:
                del self.pending_qkd[session_id]
            # Remove encryption session
            encryption_manager.remove_session_cipher(session_id)

        # Notify remaining users
        await self.broadcast_user_list()

    async def send_personal_message(self, message: dict, user_id: str):
        """Send message to specific user"""
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_text(json.dumps(message))
            except:
                # Connection might be broken, remove it
                await self.disconnect(user_id)

    async def send_to_session(self, message: dict, session_id: str):
        """Send message to all users in a chat session"""
        print(f"send_to_session called for session {session_id}")
        if session_id in self.chat_sessions:
            session = self.chat_sessions[session_id]
            user_ids = [session["user1"], session["user2"]]
            print(f"Sending message to users in session: {user_ids}")
            for user_id in user_ids:
                print(f"Sending message to user {user_id}")
                await self.send_personal_message(message, user_id)
        else:
            print(f"Session {session_id} not found in chat_sessions")

    async def broadcast_user_list(self):
        """Broadcast current user list to all connected users"""
        user_list = list(self.users.values())
        message = {"type": "user_list", "users": user_list}

        # Create a copy of the keys to avoid dictionary changed size during iteration
        connection_ids = list(self.active_connections.keys())
        for user_id in connection_ids:
            await self.send_personal_message(message, user_id)

    async def initiate_qkd_handshake(self, initiator_id: str, target_id: str) -> bool:
        """Initiate QKD handshake between two users"""
        if target_id not in self.active_connections:
            return False

        session_id = create_session_key_hash(initiator_id, target_id)

        # Store pending QKD session
        self.pending_qkd[session_id] = {
            "initiator": initiator_id,
            "target": target_id,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
        }

        # Notify target user about incoming QKD request
        await self.send_personal_message(
            {
                "type": "qkd_request",
                "session_id": session_id,
                "from_user": self.users[initiator_id]["display_name"],
                "from_user_id": initiator_id,
            },
            target_id,
        )

        # Notify initiator
        await self.send_personal_message(
            {
                "type": "qkd_initiated",
                "session_id": session_id,
                "target_user": self.users[target_id]["display_name"],
                "status": "waiting_for_acceptance",
            },
            initiator_id,
        )

        return True

    async def accept_qkd_handshake(self, session_id: str, user_id: str) -> bool:
        """Accept QKD handshake and perform key exchange"""
        if session_id not in self.pending_qkd:
            return False

        qkd_session = self.pending_qkd[session_id]
        if qkd_session["target"] != user_id:
            return False

        # Update status
        qkd_session["status"] = "performing_qkd"

        # Notify both users that QKD is starting
        await self.send_personal_message(
            {
                "type": "qkd_status",
                "session_id": session_id,
                "status": "performing_qkd",
                "message": "Performing quantum key distribution...",
            },
            qkd_session["initiator"],
        )

        await self.send_personal_message(
            {
                "type": "qkd_status",
                "session_id": session_id,
                "status": "performing_qkd",
                "message": "Performing quantum key distribution...",
            },
            user_id,
        )

        # Simulate QKD delay
        await asyncio.sleep(2)

        # Perform QKD (simulate small chance of eavesdropper detection)
        import random

        simulate_eavesdropper = random.random() < 0.1  # 10% chance

        print(f"Performing QKD with eavesdropper simulation: {simulate_eavesdropper}")
        session_key, eavesdropper_detected = generate_session_key(
            qkd_session["initiator"], qkd_session["target"], simulate_eavesdropper
        )

        print(
            f"QKD result - Key: {session_key is not None}, Eavesdropper: {eavesdropper_detected}"
        )

        if eavesdropper_detected or not session_key:
            # QKD failed - eavesdropper detected
            await self.send_personal_message(
                {
                    "type": "qkd_failed",
                    "session_id": session_id,
                    "reason": "eavesdropper_detected",
                    "message": "⚠️ Security breach detected! Connection terminated.",
                },
                qkd_session["initiator"],
            )

            await self.send_personal_message(
                {
                    "type": "qkd_failed",
                    "session_id": session_id,
                    "reason": "eavesdropper_detected",
                    "message": "⚠️ Security breach detected! Connection terminated.",
                },
                user_id,
            )

            # Clean up
            del self.pending_qkd[session_id]
            return False

        # QKD successful - establish secure session
        print(f"QKD successful, setting up encryption for session {session_id}")
        success = encryption_manager.create_session_cipher(session_id, session_key)
        print(f"Encryption setup result: {success}")

        if not success:
            await self.send_personal_message(
                {
                    "type": "qkd_failed",
                    "session_id": session_id,
                    "reason": "encryption_setup_failed",
                    "message": "Failed to establish encryption. Please try again.",
                },
                qkd_session["initiator"],
            )

            await self.send_personal_message(
                {
                    "type": "qkd_failed",
                    "session_id": session_id,
                    "reason": "encryption_setup_failed",
                    "message": "Failed to establish encryption. Please try again.",
                },
                user_id,
            )

            del self.pending_qkd[session_id]
            return False

        # Create chat session
        self.chat_sessions[session_id] = {
            "user1": qkd_session["initiator"],
            "user2": qkd_session["target"],
            "established_at": datetime.now().isoformat(),
            "status": "active",
        }

        # Get key fingerprint for verification
        key_fingerprint = encryption_manager.get_session_fingerprint(session_id)
        print(f"Generated key fingerprint: {key_fingerprint}")

        # Notify both users of successful connection
        success_message = {
            "type": "qkd_success",
            "session_id": session_id,
            "key_fingerprint": key_fingerprint,
            "message": "🔐 Secure quantum channel established!",
        }

        print(f"Sending QKD success messages to both users")
        await self.send_personal_message(
            {
                **success_message,
                "chat_partner": self.users[user_id]["display_name"],
                "chat_partner_id": user_id,
            },
            qkd_session["initiator"],
        )

        await self.send_personal_message(
            {
                **success_message,
                "chat_partner": self.users[qkd_session["initiator"]]["display_name"],
                "chat_partner_id": qkd_session["initiator"],
            },
            user_id,
        )

        print(f"QKD handshake completed successfully for session {session_id}")

        # Clean up pending QKD
        del self.pending_qkd[session_id]
        return True

    async def reject_qkd_handshake(self, session_id: str, user_id: str) -> bool:
        """Reject QKD handshake"""
        if session_id not in self.pending_qkd:
            return False

        qkd_session = self.pending_qkd[session_id]
        if qkd_session["target"] != user_id:
            return False

        # Notify initiator of rejection
        await self.send_personal_message(
            {
                "type": "qkd_rejected",
                "session_id": session_id,
                "message": f"{self.users[user_id]['display_name']} declined the secure chat request.",
            },
            qkd_session["initiator"],
        )

        # Clean up
        del self.pending_qkd[session_id]
        return True

    async def send_encrypted_message(
        self, session_id: str, sender_id: str, message: str
    ):
        """Send encrypted message in a secure session"""
        print(f"Attempting to send encrypted message in session {session_id}")
        if session_id not in self.chat_sessions:
            print(f"Session {session_id} not found in chat_sessions")
            await self.send_personal_message(
                {"type": "error", "message": "Chat session not found"}, sender_id
            )
            return

        # Encrypt the message
        print(f"Encrypting message: {message}")
        encrypted_message = encryption_manager.encrypt_message(session_id, message)
        print(f"Encrypted message result: {encrypted_message is not None}")
        if not encrypted_message:
            await self.send_personal_message(
                {"type": "error", "message": "Failed to encrypt message"}, sender_id
            )
            return

        # Send to both users in the session
        chat_message = {
            "type": "chat_message",
            "session_id": session_id,
            "sender_id": sender_id,
            "sender_name": self.users[sender_id]["display_name"],
            "encrypted_message": encrypted_message,
            "timestamp": datetime.now().isoformat(),
        }

        print(f"Sending chat message to session {session_id}: {chat_message}")
        await self.send_to_session(chat_message, session_id)

    async def send_encrypted_image(
        self,
        session_id: str,
        sender_id: str,
        image_data: str,
        filename: str,
        file_type: str,
    ):
        """Send encrypted image in a secure session"""
        print(f"Attempting to send encrypted image in session {session_id}")
        if session_id not in self.chat_sessions:
            print(f"Session {session_id} not found in chat_sessions")
            await self.send_personal_message(
                {"type": "error", "message": "Chat session not found"}, sender_id
            )
            return

        # Compress image if needed
        try:
            # Decode base64 image
            image_bytes = base64.b64decode(
                image_data.split(",")[1] if "," in image_data else image_data
            )

            # Compress image to reduce size
            image = Image.open(io.BytesIO(image_bytes))

            # Resize if too large (max 800px on longest side)
            max_size = 800
            if max(image.size) > max_size:
                ratio = max_size / max(image.size)
                new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
                image = image.resize(new_size, Image.Resampling.LANCZOS)

            # Convert to RGB if necessary
            if image.mode in ("RGBA", "LA"):
                background = Image.new("RGB", image.size, (255, 255, 255))
                background.paste(
                    image, mask=image.split()[-1] if image.mode == "RGBA" else None
                )
                image = background

            # Save compressed image
            output = io.BytesIO()
            image.save(output, format="JPEG", quality=85, optimize=True)
            compressed_data = base64.b64encode(output.getvalue()).decode()

            print(
                f"Image compressed from {len(image_bytes)} to {len(output.getvalue())} bytes"
            )

        except Exception as e:
            print(f"Image processing error: {e}")
            compressed_data = image_data

        # Create image message payload
        image_payload = {
            "data": compressed_data,
            "filename": filename,
            "type": file_type,
            "size": len(compressed_data),
        }

        # Encrypt the image data
        print(f"Encrypting image data")
        encrypted_image = encryption_manager.encrypt_message(
            session_id, json.dumps(image_payload)
        )
        print(f"Image encryption result: {encrypted_image is not None}")
        if not encrypted_image:
            await self.send_personal_message(
                {"type": "error", "message": "Failed to encrypt image"}, sender_id
            )
            return

        # Send to both users in the session
        image_message = {
            "type": "image_message",
            "session_id": session_id,
            "sender_id": sender_id,
            "sender_name": self.users[sender_id]["display_name"],
            "encrypted_image": encrypted_image,
            "filename": filename,
            "timestamp": datetime.now().isoformat(),
        }

        print(f"Sending image message to session {session_id}")
        await self.send_to_session(image_message, session_id)


# Global connection manager
manager = ConnectionManager()


class DecryptRequest(BaseModel):
    session_id: str
    encrypted_message: str


class ImageUploadRequest(BaseModel):
    session_id: str
    image_data: str  # Base64 encoded image
    filename: str
    file_type: str


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket, user_id: str, display_name: str = "Anonymous"
):
    """Main WebSocket endpoint for chat"""
    await manager.connect(websocket, user_id, display_name)

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            message_type = message.get("type")
            print(f"Received message from {user_id}: {message_type}")

            if message_type == "initiate_qkd":
                target_id = message.get("target_user_id")
                print(f"Initiating QKD between {user_id} and {target_id}")
                if target_id:
                    await manager.initiate_qkd_handshake(user_id, target_id)

            elif message_type == "accept_qkd":
                session_id = message.get("session_id")
                print(f"Accepting QKD for session {session_id}")
                if session_id:
                    await manager.accept_qkd_handshake(session_id, user_id)

            elif message_type == "reject_qkd":
                session_id = message.get("session_id")
                if session_id:
                    await manager.reject_qkd_handshake(session_id, user_id)

            elif message_type == "chat_message":
                session_id = message.get("session_id")
                msg_content = message.get("message")
                print(
                    f"Chat message from {user_id} in session {session_id}: {msg_content}"
                )
                if session_id and msg_content:
                    await manager.send_encrypted_message(
                        session_id, user_id, msg_content
                    )

            elif message_type == "image_message":
                session_id = message.get("session_id")
                image_data = message.get("image_data")
                filename = message.get("filename", "image.jpg")
                file_type = message.get("file_type", "image/jpeg")
                print(f"Image message from {user_id} in session {session_id}")
                if session_id and image_data:
                    await manager.send_encrypted_image(
                        session_id, user_id, image_data, filename, file_type
                    )

            elif message_type == "ping":
                await manager.send_personal_message(
                    {"type": "pong", "timestamp": datetime.now().isoformat()}, user_id
                )

    except WebSocketDisconnect:
        await manager.disconnect(user_id)
    except Exception as e:
        print(f"WebSocket error for user {user_id}: {e}")
        await manager.disconnect(user_id)


@app.post("/api/decrypt-message")
async def decrypt_message_endpoint(request: DecryptRequest):
    """Decrypt a message for display"""
    try:
        # Log detailed information for debugging
        print(f"Attempting to decrypt message for session: {request.session_id}")
        print(f"Available session ciphers: {list(encryption_manager.session_ciphers.keys())}")
        
        decrypted = encryption_manager.decrypt_message(
            request.session_id, request.encrypted_message
        )
        if decrypted:
            return {"decrypted_message": decrypted}
        else:
            print(f"Decryption failed for session {request.session_id}: No result returned")
            return JSONResponse(
                status_code=400,
                content={"error": f"Failed to decrypt message. Session may not exist."}
            )
    except Exception as e:
        print(f"Decryption error for session {request.session_id}: {str(e)}")
        return JSONResponse(
            status_code=500, 
            content={"error": f"Decryption failed: {str(e)}"}
        )


@app.post("/api/decrypt-image")
async def decrypt_image_endpoint(request: DecryptRequest):
    """Decrypt an image for display"""
    try:
        # Log detailed information for debugging
        print(f"Attempting to decrypt image for session: {request.session_id}")
        print(f"Available session ciphers: {list(encryption_manager.session_ciphers.keys())}")
        
        decrypted = encryption_manager.decrypt_message(
            request.session_id, request.encrypted_message
        )
        if decrypted:
            # Parse the decrypted JSON image payload
            try:
                image_payload = json.loads(decrypted)
                return {
                    "image_data": image_payload["data"],
                    "filename": image_payload["filename"],
                    "file_type": image_payload["type"],
                    "size": image_payload["size"],
                }
            except json.JSONDecodeError as je:
                print(f"JSON parsing error for decrypted image: {str(je)}")
                return JSONResponse(
                    status_code=400,
                    content={"error": f"Failed to parse decrypted image data: {str(je)}"}
                )
        else:
            print(f"Image decryption failed for session {request.session_id}: No result returned")
            return JSONResponse(
                status_code=400,
                content={"error": f"Failed to decrypt image. Session may not exist."}
            )
    except Exception as e:
        print(f"Image decryption error for session {request.session_id}: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Image decryption failed: {str(e)}"}
        )


@app.get("/")
async def root():
    """API health check"""
    return {"message": "Quantum Chat API is running", "version": "1.0.0"}


@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "active_connections": len(manager.active_connections),
        "active_sessions": len(manager.chat_sessions),
        "pending_qkd": len(manager.pending_qkd),
        "timestamp": datetime.now().isoformat(),
    }


# Removed duplicate endpoint definition


@app.post("/api/upload-file")
async def upload_file(file: UploadFile = File(...), session_id: str = None):
    """Upload and encrypt a file for sharing"""
    try:
        if not session_id:
            raise HTTPException(status_code=400, detail="session_id is required")

        if session_id not in manager.chat_sessions:
            raise HTTPException(status_code=404, detail="Chat session not found")

        # Read file data
        file_data = await file.read()

        # Encrypt file
        cipher = encryption_manager.get_session_cipher(session_id)
        if not cipher:
            raise HTTPException(
                status_code=400, detail="Encryption not available for session"
            )

        encrypted_data = cipher.encrypt_file(file_data)

        # For demo purposes, we'll store the encrypted file temporarily
        # In production, you'd want to use proper file storage (S3, etc.)
        file_id = str(uuid.uuid4())

        # Convert to base64 for JSON transport
        encrypted_b64 = base64.b64encode(encrypted_data).decode("utf-8")

        return {
            "file_id": file_id,
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(file_data),
            "encrypted_data": encrypted_b64,  # In production, store this securely
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
