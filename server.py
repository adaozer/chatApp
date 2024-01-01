import socket
import threading
import sys

port = int(sys.argv[1])
activeClients = {}

# https://www.youtube.com/watch?v=Cqoqd31BbwI&t=1155s&ab_channel=AllAboutPython
# https://docs.python.org/3/library/socket.html
# https://python.plainenglish.io/building-a-messaging-app-with-python-sockets-and-threads-1c110fc1c8c8
# https://www.geeksforgeeks.org/simple-chat-room-using-python/

# def receiveMessage(client):
    
#     while True:
#         try:
#             message = client.recv(2048).decode("utf-8")
#             username = activeClients[client]

#             if "/msg" in message:
#                 splitMessage = message.split()
#                 receiver = splitMessage[1]
                
#                 # https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/

#                 dictKeys = list(activeClients.keys())
#                 dictValues = list(activeClients.values())
#                 pos = dictValues.index(receiver)
#                 receiverSocket = dictKeys[pos]

#                 #for socket, user in activeClients.items():
#                  #   if user == receiver:
#                   #      receiverSocket = socket
                
#                 messageFinal = " ".join(splitMessage[2:])
#                 sendUni = username + ": " + messageFinal
#                 receiverSocket.sendall(sendUni.encode("utf-8"))

#             else:
#                 sendBroad = username + ": " + message
#                 broadcast(client, sendBroad)

#         except KeyboardInterrupt: 
#             print("Message failed to send")

def unicast(username, message):

    splitMessage = message.split()
    receiver = splitMessage[1]
                    
    # https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/

    dictKeys = list(activeClients.keys())
    dictValues = list(activeClients.values())
    pos = dictValues.index(receiver)
    receiverSocket = dictKeys[pos]

    #for socket, user in activeClients.items():
    #   if user == receiver:
    #      receiverSocket = socket
                    
    messageFinal = " ".join(splitMessage[2:])
    sendUni = username + ": " + messageFinal
    receiverSocket.sendall(sendUni.encode("utf-8"))


    
def broadcast(client, message):
    for clients in activeClients:
        if clients != client: 
            clients.sendall(message.encode('utf-8'))


def clientLeave(client):
    username = activeClients[client]
    broadcast(client, f"{username} has left!")
    activeClients.pop(client)
    client.close()


def clientAdd(client, address):
    print(f"Connection from {address}")
    try:
        username = client.recv(2048).decode("utf-8")
        activeClients[client] = username  
        hello = f"{username} has joined!"
        broadcast(client, hello) 
        client.sendall(f"Welcome to the server {username}!".encode('UTF-8'))

    except:
        print("Client could not connect!")

    #threading.Thread(target=receiveMessage, args=(client, )).start()

    while True:
        try:
            message = client.recv(2048).decode("utf-8")
            username = activeClients[client]

            if "/msg" in message:
                unicast(username, message)

            elif message == "/leave":
                clientLeave(client)

            else:
                sendBroad = username + ": " + message
                broadcast(client, sendBroad)

        except KeyboardInterrupt:
            clientLeave(client) 
        
        except OSError:
            pass

        except:
            print("Message failed to send")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("", port))
            print(f"Server has started at {port}")
        except:
            print(f"Server unable to be bound to {port}")
        
        s.listen()

        while True:
            
            client, address = s.accept()
            threading.Thread(target=clientAdd, args=(client, address, )).start()
        

if __name__ == "__main__":
    main()
