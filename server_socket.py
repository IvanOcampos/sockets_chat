import socket
import threading

#Server configuration
HOST = "127.0.0.1"
PORT = 8081

#Server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print(f"✅ Server running on {HOST}:{PORT}")

#List to track clients and usernames
clients = []
usernames = []

def broadcast(message, _client):
    """
    Sends a message to all clients except the sender (_client)
    """
    for client in clients:
        if client != _client:
            try:
                client.send(message)
                
            except Exception as e:
                print(f"⚠ Could not send to a client: {e}")
        
def handle_messages(client):
    """
    Handles messages from a single client
    Detects diconnections and cleans up client data
    """
    while True:
        try:
            message = client.recv(1024)
            
            #If recv returns empty, client disconnected
            if not message:
                raise ConnectionError("Client disconnected")
            
            #Get username of sender
            index = clients.index(client)
            username = usernames[index]
            
            #Print and broadcast message
            print(f"[MSG] {message.decode('utf-8')}")
            broadcast(message, client)
            
        except Exception:
            #Client disconnected or error occured
            if client in clients:
                index = clients.index(client)
                username = usernames[index]
            
                print(f"[-] {username} disconnected")

                #Inform other clients
                broadcast(f"ChatBot: {username} disconnected".encode("utf-8"), client)
            
                #Clean up
                clients.remove(client)
                usernames.remove(username)
                try:
                    client.close()
                except:
                    pass
            break
        
def receive_connections():
    """
    Accepts new client conections and starts a thread for each client
    """
    while True:
        try:
            client, address = server.accept() 
        
            #Handshake: ask for username
            client.send("@username".encode("utf-8"))
            username = client.recv(1024).decode("utf-8")
            
            #Save client info
            clients.append(client)
            usernames.append(username)
            
            print(f"[+] {username} connected from {(address)}")
            
            #Welcome message to others
            message = f"ChatBot: {username} joined the chat!".encode("utf-8")
            broadcast(message, client)
            client.send("Connected to server".encode("utf-8"))
        
            #Start thread to handle messages
            thread = threading.Thread(target=handle_messages, args=(client,))
            thread.start()
        
        except Exception as e:
            print(f"⚠ Error accepting a new connection: {e}")

receive_connections()