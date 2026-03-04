# Python Chat Application (Client & Server)

A simple TCP chat application in Python using `socket` and `threading`, supporting multiple clients, message broadcasting, and automatic reconnection.

---

## Features

- **Multi-client support**: Multiple users can connect to the server simultaneously.  
- **Broadcasting**: Messages are sent to all connected clients except the sender.  
- **Username handshake**: Clients provide a username upon connecting.  
- **Connection management**: Detects client disconnections and cleans up.  
- **Automatic client reconnection**: Clients keep trying to reconnect if the server is unavailable.  
- **Error handling**: Graceful handling of exceptions and lost connections.  

---

## Server (`server_socket.py`)

### How it works

1. **Socket setup**: Creates a TCP socket bound to `HOST` and `PORT`.  
2. **Accepting connections**: Continuously accepts new clients and asks for their username.  
3. **Message handling**: Each client runs in a separate thread. Messages are received and broadcast to other clients.  
4. **Disconnection handling**: If a client disconnects or an error occurs, it removes the client and informs others.  

### Usage

```bash
python server_socket.py
```