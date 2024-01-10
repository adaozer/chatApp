import socket
import threading
import sys
import os


username = sys.argv[1]
host = sys.argv[2]
port = int(sys.argv[3]) # Get the username, host, port information from the arguements.
currentDir = os.getcwd()
downloadDir = f"{currentDir}/{username}"

def receiveMessage(client):

    while True:
        try:
            message = client.recv(2048).decode('utf-8') # Constantly check for data coming from the server.
            if "**start**" in message: # For download functionality
                split = message.split()
                filename = split[1] # Get the filename
                # Vinod Sharma. (2015, March 18). How to download file from local server in Python. Stack Overflow. https://stackoverflow.com/questions/29110620/how-to-download-file-from-local-server-in-python 
                with open(os.path.join(downloadDir, filename), 'wb') as file: # Open the file
                    while True:
                        data = client.recv(1024) # Receive all data from the file
                        if "**end**" in data.decode('utf-8', 'ignore'): # End of the data is indicated.
                            file.write(data[:data.find(b"**end**")]) # Write until the end of the data
                            print("File downloaded.")
                            break
                        file.write(data) # Write in the file the data received from the server
            else:
                print(message) # Print message as usual if there isn't a download coming in.
        except ConnectionAbortedError and ConnectionResetError and OSError: # Exception handling
            print("Connection aborted.")
            client.close()
            break
        except:
            print("An error occured.")

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