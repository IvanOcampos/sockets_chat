import socket
import threading
import time

#Server configuration
HOST = "127.0.0.1"
PORT = 8081


#Ask username once at the beginnig 
username = input("Enter your username: ")

#Global variable to track connection state
connected = False

def connect_to_server():
    """
    Tries to connect to the server
    If the server is unavailable, it keeps retrying every 5 seconds.
    """
    global client, connected
    
    while True:
        try:
            #Create a new socket every time we attempt to reconnect
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST, PORT))
            
            connected = True
            print("\n✔ Conneted to server\n")
            break
        
        except ConnectionRefusedError:
            print("\n❌ Server unavailable. Reconnecting in 5 seconds...\n")
            time.sleep(5)

def receive_message():
    """
    Continuosly listens for messages from the server
    If the server disconnects, it attempts to reconnect automatically
    """
    global connected
    
    while True:
        #If not connected, try to reconnect
        if not connected:
            connect_to_server()
            
        try:
            message = client.recv(1024)
            
            #If recv returns empty, server closed connection
            if not message:
                raise Exception("Server disconnected")
            
            message = message.decode("utf-8")
            
            #Handshaeke logic: server asks for username
            if message == "@username":
                client.send(username.encode("utf-8"))
            else:
                print(message)
        
        except Exception:
            print("⚠ Lost connection with server.")
            connected = False

            try:
                client.close()
            
            except:
                pass
            
            #Small delay before trying again
            time.sleep(2)

        
def write_messages():
    """
    Continously  takes user input and sends messages to the server
    If not connected, it prevents sending
    """
    global connected
    
    while True:
        message = input()
        
        if connected:
            try:
                client.send(f"{username}: {message}".encode("utf-8"))
            
            except:
                connected = False
        
        else:
            print("⛔ Not connected. Message not sent.")

#Initial connection attempt
connect_to_server()

#Start threads
receive_thread = threading.Thread(target = receive_message)
receive_thread.start()

write_thread = threading.Thread(target = write_messages)
write_thread.start()