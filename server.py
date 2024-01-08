import socket
import threading
import sys
import logging

port = int(sys.argv[1]) # Get the desired port from the arguements.
activeClients = {} # Initialize active clients dictionary for storing socket and username information.
logging.basicConfig(filename='server.log', filemode='a+', level=logging.INFO) # Set up server.log file.

# https://www.youtube.com/watch?v=Cqoqd31BbwI&t=1155s&ab_channel=AllAboutPython
# https://docs.python.org/3/library/socket.html
# https://python.plainenglish.io/building-a-messaging-app-with-python-sockets-and-threads-1c110fc1c8c8
# https://python.plainenglish.io/building-a-messaging-app-with-python-sockets-and-threads-continue-b7b344ff6e76
# https://www.geeksforgeeks.org/simple-chat-room-using-python/
# https://docs.python.org/3/howto/logging.html
# https://docs.python.org/3/library/logging.html

def unicast(username, message):

    splitMessage = message.split()
    receiver = splitMessage[1] # Access username of the recepient of the message.
    # https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/

    dictKeys = list(activeClients.keys())
    dictValues = list(activeClients.values())
    pos = dictValues.index(receiver)
    receiverSocket = dictKeys[pos] # Access the socket information of the recepient of the message.
                    
    messageFinal = " ".join(splitMessage[2:])
    sendUni = username + ": " + messageFinal
    logging.info(f"{username} sent a private message to {receiver} with the content: {messageFinal}") #
    receiverSocket.sendall(sendUni.encode("utf-8")) # Create the final message in the correct format and send it to the recepient.

    
def broadcast(client, message):
    for clients in activeClients:
        if clients != client: # Broadcast the message to everyone who isn't the original sender.
            clients.sendall(message.encode('utf-8')) 

def clientLeave(client):
    username = activeClients[client]
    broadcast(client, f"{username} has left!") # Broacast to all other clients that the user left.
    logging.info(f"Server broadcasted to the clients that {username} left the server.")
    activeClients.pop(client) # Remove the client from the active clients dictionary.
    client.close() # Close the client's port to finish the client leaving process.


def clientAdd(client, address):
    print(f"Connection from {address}")
    try:
        username = client.recv(2048).decode("utf-8")
        logging.info(f'{username} joined from the port {address}') # Log and print the source of the incoming connection.
        activeClients[client] = username # Add the new client to the active clients dictionary. 
        hello = f"{username} has joined!"
        broadcast(client, hello) 
        logging.info(f"Server broadcasted to the clients that {username} joined the server.")
        client.sendall(f"Welcome to the server {username}!".encode('UTF-8')) # Broadcast to all other users that a new user has joined and log the necessary information.

    except:
        print("Client could not connect!") # Handle exceptions.

    while True:
        try:
            message = client.recv(2048).decode("utf-8") # Constantly check for incoming data from the client socket.
            username = activeClients[client] 

            if "/msg" in message: # Check if the message is unicast or broadcast.
                unicast(username, message)

            elif message == "/leave": # Check if the message is a leave command.
                clientLeave(client)
                logging.info(f"{username} left the server.")
                break

            else:
                sendBroad = username + ": " + message
                broadcast(client, sendBroad)
                logging.info(f"{username} broadcasted a message with the content: {message}") # Act accordingly to the previous info and log the result.

        except KeyboardInterrupt:
            clientLeave(client) 
            logging.info(f"{username} left the server.") # Check if user input a leave command and log it.
            break

        except ConnectionResetError:
            clientLeave(client) 
            logging.error(f"{username} has disconnected unexpectedly.") # Check if a user crashed and log it.
            break

        except:
            errorMessage = "Message failed to send."
            print(errorMessage)
            logging.error(f"A message failed to send from {username}")
            client.sendall(errorMessage.encode('utf-8')) # Handle exceptions by logging it and broadcasting it to the clients.

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("", port)) # Initialize server at the inputted port.
            print(f"Server has started at {port}") # Print that the server has started and log it in the server.log file.
            logging.info(f"Server started at {port}")
        except:
            print(f"Server unable to be bound to {port}") # Handle errors by printing the necessary information and logging it.
            logging.critical(f"Server unable to be bound to {port}")

        s.listen() # Listen for connections.

        while True:
                client, address = s.accept() 
                threading.Thread(target=clientAdd, args=(client, address, )).start() # Accept connections and create a thread for each client.

if __name__ == "__main__":
    main()
