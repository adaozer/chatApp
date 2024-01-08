**Computer Science Year 2 Networks and Systems Project**

------------------------------

Introduction:

This is the cmd chat application project for the Networks and Systems module. This readme.txt file includes information 
about how to run the server and use the features.

------------------------------

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
ctrl+c. To close the server, simply run keyboard interrupt ctrl+c. When another client tries to join the server, 
they will be denied and won't be able to send any messages. This will also be the case for existing clients.

Checking the server.log file will provide a log of all activities that have happened in the server.

------------------------------

References:

- AllAboutPython. (2021, October 10). How to create a real time chat app in python using socket programming | part 2. YouTube. https://www.youtube.com/watch?v=Cqoqd31BbwI&t=1155s&ab_channel=AllAboutPython 
- GeeksForGeeks. (2022, February 19). Simple chat room using Python. GeeksforGeeks. https://www.geeksforgeeks.org/simple-chat-room-using-python/ 
- GeeksforGeeks. (2023, May 4). Python: Get key from value in dictionary. https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/ 
- Hannu. (2017, June 6). Python sockets - how to shut down the server?. Stack Overflow. https://stackoverflow.com/questions/44387712/python-sockets-how-to-shut-down-the-server 
- Logging - logging facility for Python. Python documentation. (n.d.-a). https://docs.python.org/3/library/logging.html 
- Logging howto. Python documentation. (n.d.-b). https://docs.python.org/3/howto/logging.html 
- Raychev, J. P. (2021a, February 19). Building a messaging app with python sockets and threads. Medium. https://python.plainenglish.io/building-a-messaging-app-with-python-sockets-and-threads-continue-b7b344ff6e76 
- Raychev, J. P. (2021b, November 17). Building a messaging app with python sockets and threads. Medium. https://python.plainenglish.io/building-a-messaging-app-with-python-sockets-and-threads-1c110fc1c8c8 
- Socket - low-level networking interface. Python documentation. (n.d.-c). https://docs.python.org/3/library/socket.html 