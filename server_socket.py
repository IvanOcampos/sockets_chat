import socket
import threading

HOST = "127.0.0.1"
PORT = 8081

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Le paso de parametro que vamos a utilizar el tipo de conexion IPv4 y el protocolo TCP

server.bind((HOST, PORT))
server.listen()
print(f"Server running on {HOST}:{PORT}")

clients = []
usernames = []

def broadcast(message, _client):
    for client in clients:
        if _client != client:
            client.send(message)
        

def handle_messages(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            index = clients.index(client)
            username = usernames[index]
            broadcast(f"ChatBot: {username} disconnected".encode("utf-8"), client)
            clients.remove(client)
            usernames.remove(username)
            client.close()
            break
        
def receive_connections():
    while True:
        client, addres = server.accept() 
        
        client.send("@username".encode("utf-8"))
        username = client.recv(1024).decode("utf-8")
        
        clients.append(client)
        usernames.append(username)
        
        print(f"{username} is connected with {str(addres)}")
        
        message = f"ChatBot: {username} joined the chat!".encode("utf-8")
        broadcast(message, client)
        client.send("Connected to sercer".encode("utf-8"))
    
        #Hilos
        thread = threading.Thread(target=handle_messages, args=(client,))
        thread.start()

receive_connections()