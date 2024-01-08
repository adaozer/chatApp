Files included:

- server.py
- client.py
- server.log
- README.txt

------------------------------

Running instructions:

Put all files in the same directory. Start the server by inputting "python server.py [port]" to a cmd
window pointing at the correct directory where [port] is the port you want to start the file in.

Connect a client to the server by running "python client.py [username] [host] [port]" to a cmd
window pointing at the correct directory where [username] is what the client's name will be displayed
as in the server, and [host] and [port] is the host and port they'll connect from.

------------------------------

How the chat app works:

Writing in the cmd window and pressing enter will broadcast a message to all active clients in the server.
To unicast a message to a specific user, simply put "/msg [username] [message]" in the cmd window where
[username] is the username of the client you want to unicast to, and [message] is the message you want
to send.

To leave the server, clients can either input "/leave" in the cmd window or simply run keyboard interrupt
ctrl+c. To close the server, simply run keyboard interrupt ctrl+c twice.

Checking the server.log file will provide a log of all activities that have happened in the server.