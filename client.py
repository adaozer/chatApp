import socket
import threading
import sys


username = sys.argv[1]
host = sys.argv[2]
port = int(sys.argv[3]) # Get the username, host, port information from the arguements.

def receiveMessage(client):

    while True:
        try:
            message = client.recv(2048).decode('utf-8') # Constantly check for data coming from the server.
            print(message)
        except ConnectionAbortedError and ConnectionResetError and OSError:
            print("Connection aborted.")
            client.close()
            break

def clientStart():
    serverAdress = (host, port)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Set up the client socket.
    try:
        clientSocket.connect(serverAdress)
        clientSocket.sendall(username.encode("utf-8")) # Connect to the server address and send the username data to the server.
    except:
        print("Failed to connect to the server!") # Handle exceptions.
    
    try:
        welcome = clientSocket.recv(2048).decode("utf-8")
        print(welcome) # Receive welcome message from the server.
    except ConnectionResetError:
        print("Couldn't connect to server!")
        clientSocket.close()

    threading.Thread(target=receiveMessage, args=(clientSocket, )).start() # Start a thread waiting for data from the server for each client.

    while True:
        try:
            message = input()
            clientSocket.sendall(message.encode('utf-8')) # Constantly available messaging feature, check if the client is sending any messages.

# Hannu. (2017, June 6). Python sockets - how to shut down the server?. Stack Overflow. https://stackoverflow.com/questions/44387712/python-sockets-how-to-shut-down-the-server             
      
        except KeyboardInterrupt:
            clientSocket.sendall("/leave".encode('utf-8'))
            clientSocket.close()
            sys.exit(0) # When the client uses keyboard interrupt,  
        except OSError:
            print("Server is closed, message couldn't send.")
            clientSocket.close()
            break

if __name__ == "__main__":
    clientStart()