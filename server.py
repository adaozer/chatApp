import socket
import threading
import sys
import logging

port = int(sys.argv[1])
activeClients = {}
logging.basicConfig(filename='server.log', filemode='a+', level=logging.INFO)

# https://www.youtube.com/watch?v=Cqoqd31BbwI&t=1155s&ab_channel=AllAboutPython
# https://docs.python.org/3/library/socket.html
# https://python.plainenglish.io/building-a-messaging-app-with-python-sockets-and-threads-1c110fc1c8c8
# https://python.plainenglish.io/building-a-messaging-app-with-python-sockets-and-threads-continue-b7b344ff6e76
# https://www.geeksforgeeks.org/simple-chat-room-using-python/
# https://docs.python.org/3/howto/logging.html
# https://docs.python.org/3/library/logging.html

def unicast(username, message):

    splitMessage = message.split()
    receiver = splitMessage[1]            
    # https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/

    dictKeys = list(activeClients.keys())
    dictValues = list(activeClients.values())
    pos = dictValues.index(receiver)
    receiverSocket = dictKeys[pos]
                    
    messageFinal = " ".join(splitMessage[2:])
    sendUni = username + ": " + messageFinal
    logging.info(f"{username} sent a private message to {receiver} with the content: {messageFinal}")
    receiverSocket.sendall(sendUni.encode("utf-8"))

    
def broadcast(client, message):
    for clients in activeClients:
        if clients != client: 
            clients.sendall(message.encode('utf-8'))

def clientLeave(client):
    username = activeClients[client]
    broadcast(client, f"{username} has left!")
    logging.info(f"Server broadcasted to the clients that {username} left the server.")
    activeClients.pop(client)
    client.close()


def clientAdd(client, address):
    print(f"Connection from {address}")
    try:
        username = client.recv(2048).decode("utf-8")
        activeClients[client] = username  
        hello = f"{username} has joined!"
        broadcast(client, hello) 
        logging.info(f"Server broadcasted to the clients that {username} joined the server.")
        client.sendall(f"Welcome to the server {username}!".encode('UTF-8'))
        logging.info(f'{username} joined the server from port {address}')

    except:
        print("Client could not connect!")

    while True:
        try:
            message = client.recv(2048).decode("utf-8")
            username = activeClients[client]

            if "/msg" in message:
                unicast(username, message)

            elif message == "/leave":
                clientLeave(client)
                logging.info(f"{username} left the server.")
                break

            else:
                sendBroad = username + ": " + message
                broadcast(client, sendBroad)
                logging.info(f"{username} broadcasted a message with the content: {message}")

        except KeyboardInterrupt:
            clientLeave(client) 
            logging.info(f"{username} left the server.")
            break

        except ConnectionResetError:
            clientLeave(client) 
            logging.error(f"{username} has disconnected unexpectedly.")
            break

       # except:
        #    errorMessage = "Message failed to send."
         #   print(errorMessage)
          #  logging.error(f"A message failed to send from {username}")
           # client.sendall(errorMessage.encode('utf-8'))

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("", port))
            print(f"Server has started at {port}")
            logging.info(f"Server started at {port}")
        except:
            print(f"Server unable to be bound to {port}")
            logging.critical(f"Server unable to be bound to {port}")

        s.listen()

        while True:
            
            client, address = s.accept()
            threading.Thread(target=clientAdd, args=(client, address, )).start()
        

if __name__ == "__main__":
    main()
