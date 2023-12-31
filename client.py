import socket
import threading
import sys


username = sys.argv[1]
host = sys.argv[2]
port = int(sys.argv[3])

def sendMessage(client):
    
    while True:
        message = input("Please enter your message: ")
        client.sendall(message.encode('utf-8'))

def receiveMessage(client):

    while True:
        message = client.recv(2048).decode('utf-8')
        print(message)
   

def clientStart():
    serverAdress = (host, port)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        clientSocket.connect(serverAdress)
        clientSocket.sendall(username.encode("utf-8"))
    except:
        print("Failed to connect to the server!")

    welcome = clientSocket.recv(2048).decode("utf-8")
    print(welcome)

    threading.Thread(target=receiveMessage, args=(clientSocket, )).start()
    sendMessage(clientSocket)


if __name__ == "__main__":
    clientStart()