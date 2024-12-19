## Client Code

# imports the built-in `socket` module, which provides access to the BSD socket interface. This 
# module allows Python programs to establish network connections, send and receive data over the 
# network, and create various types of network sockets for communication.
import socket

# imports the built-in `threading` module, which provides a high-level interface for working with 
# threads in Python. By using the threading` module, the code can create and manage multiple 
# threads to perform tasks concurrently. In this case, the code is using threading to create a 
# separate thread for receiving messages from the server while allowing the main thread to handle 
# user input and sending messages. This helps in achieving asynchronous communication between the 
# client and server without blocking the main execution flow.
import threading

# Client Configuration
# setting the host IP address to `127.0.0.1`, which is the loopback address in IPv4. This address is 
# commonly used to refer to the local machine itself. In the context of networking, when a client 
# program connects to `127.0.0.1`, it is connecting to the local machine where the client program is 
# running. This allows the client to communicate with a server running on the same machine, enabling 
# local network communication.
HOST = '127.0.0.1'
# setting the port number to 5001 for the client-server communication. When a client program connects 
# to a server, it needs to specify the port number on which the server is listening for incoming 
# connections.
PORT = 5001

def receive_messages(client_socket):
    """
    The function `receive_messages`  receives and prints messages from a client socket until an
    exception occurs.
    
    :param client_socket: The `client_socket` parameter in the `receive_messages` function is expected
    to be a socket object representing a connection to a client. This socket object is used to receive
    messages from the client in the function
    """
    while True:
        try:
            # the `recv()` method is used to receive data from the connected client socket. The 
            # `.decode('utf-8')` method is used to decode a sequence of bytes into a string using  
            # the UTF-8 encoding. In this context, when data is received from the client socket 
            # using `client_socket.recv(1024)`, it is returned as a sequence of bytes. By applying 
            # `.decode('utf-8')`, these bytes are converted into a human-readable string using the 
            # UTF-8 encoding. 
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                # When a message is successfully received from the client socket, it is stored in the 
                # `message` variable. The `print(message)` statement then displays this message on the 
                # console output for the user to see.
                print(message)
        except:
            break

def start_client():
    """
    The `start_client` function establishes a connection to a server, sends user input commands, and
    listens for incoming messages in a separate thread until a "LOGOUT" command is entered.
    """
    # The line below is creating a new socket object for the client to establish a connection with the 
    # server using the TCP protocol. `socket.AF_INET` specifies the address family for the socket being
    # created. socket.SOCK_STREAM` specifies the type of socket being created as a stream socket.
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Establishing a connection from the client to a server using the TCP protocol.
    client_socket.connect((HOST, PORT))


    # Creating a new thread that will execute the `receive_messages` function concurrently with the 
    # main thread. `target=receive_messages` parameter in the `Thread` constructor is specifying the 
    # function that the new thread should execute when it starts. This allows the client program to 
    # receive and print messages from the server in a separate thread while the main thread handles 
    # user input and sending messages. By using threading in this way, the client can achieve  
    # asynchronous communication with the server without blocking the main execution flow.

    # The line `args=(client_socket,)).start()` in the code snippet is creating a new thread using the
    # `threading.Thread` class and starting that thread to execute the `receive_messages` function 
    # concurrently with the main thread.
    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    # The `while True:` loop is used to continuously receive and print messages from the client socket 
    # until an exception occurs.
    while True:
        try:
            # The line `command = input()` is responsible for taking user input from the console. When
            # this line is executed, the program waits for the user to input a command or message. The
            # input provided by the user is stored in the variable `command`, which is then processed.
            command = input()
            # The `client_socket.send` method is used to send data over the established connection
            # through the client socket. `client_socket.send(command.encode('utf-8'))` is sending the 
            # user input command entered via the console to the server and encoded into UTF-8 format.
            client_socket.send(command.encode('utf-8'))
            if command.split()[0] == "LOGOUT":
                # Check if the first word of the command is "LOGOUT". If it is, break out of the loop.
                break
        except:
            break

    client_socket.close() # close the client socket connection


start_client() # start the client connection