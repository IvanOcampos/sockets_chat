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

You will see output like:
```bash
✅ Server running on 127.0.0.1:8081
[+] Alice connected from ('127.0.0.1', 12345)
[MSG] Alice: Hello everyone
[-] Alice disconnected
```

## Client (`client_socket.py`)

### How it works

1. **Username prompt**: Asks the user for a username at the start.
2. **Connection loop**: Tries to connect to the server. If unavailable, retries every 5 seconds.
3. **Message receiving**: Continuously listens for messages from the server. Automatically handles server disconnections.
4. **Message sending**: User inputs messages, which are sent to the server and broadcast to others.

### Usage

```bash
python client_socket.py
```

You will see output like:
```bash
Enter your username: Alice
✔ Connected to server
Bob: Hello!
Alice: Hi Bob!
```

---

## Key Funtions

### Server

- `broadcast(messge, _client)`: Sends a message to all clients except _client.
- `handle_messages(client)`: Receives messages from a client, detects disconnections, and broadcast messages.
- `receive_connections()`: Continuosly accepts new client connections and stars a handler thread for each.

### Client

- `connect_to_server()`: Tries to connect to the server with retries.
- `receive_message()`: Continuosly listen for server messages. Handles server disconnections.
- `write_messages()`: Sends user input to the server if connected.

---

## Notes

- All messages are encoded/decoded in UTF-8 for network transmission.
- Disconnections are handled gracefully both on the server and client sides.
- Threads are used to allow simultaneous sending and receiving of messages.
