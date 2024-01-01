import socket
import threading
import sys


username = sys.argv[1]
host = sys.argv[2]
port = int(sys.argv[3])

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

    while True:
        try:
            message = input()
            clientSocket.sendall(message.encode('utf-8'))

        except KeyboardInterrupt:
            clientSocket.sendall("/leave".encode('utf-8'))
            clientSocket.close()
            sys.exit(0)


if __name__ == "__main__":
    clientStart()