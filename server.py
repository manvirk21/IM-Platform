## Server Code

"""
servery.py creates a server that allows users to register, login, send messages, and logout.
    - `load_users()`: Load existing users from a file.
    - `save_user(username, password)`: Save a new user to the file.
    - `broadcast(message, exclude=None)`: Send a message to all clients except the excluded one.
    - `handle_client(client_socket, addr)`: Handle client requests such as REGISTER, LOGIN, 
        LIST_ONLINE, SEND, and LOGOUT.
    - `handle_shutdown(signal, frame)`: Handle server shutdown when Ctrl+C is pressed.
    - `start_server()`: Start the server, accept client connections, and handle them in 
        separate threads.
"""

# imports the built-in `socket` module, which provides access to the BSD socket interface. This 
# module allows Python programs to establish network connections, send and receive data over the 
# network, and create various types of network sockets for communication.
import socket

# imports the built-in `threading` module, which provides a high-level interface for working  
# with threads in Python. By using the threading` module, the code can create and manage multiple 
# threads to perform tasks concurrently.
import threading

# imports the `signal` module, which provides mechanisms to work with signals and handlers in the
# operating system.
import signal

# imports the sys module in Python. The sys module provides access to some  variables used or 
# maintained by the interpreter and to functions that interact strongly with the interpreter.
import sys

# Server Configuration

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

# initializing an empty dictionary to store user information
users = {}  # Registered users (username: password)

# create an empty dictionary to store online clients
online_clients = {}  # Online clients (username: client_socket)

# Load registered users from a file
def load_users():
    """
    Load user data from a file named 'users.txt' and store it in a dictionary.
    If the file is not found, do nothing.
    """
    try:
        with open('users.txt', 'r') as file: # openning the users.txt file in read mode
            for line in file:
                # Extracting the username and password from a line of text that is formatted as 
                # "username,password".                
                username, password = line.strip().split(',')
                # add a new user with their corresponding password to the users dictionary.
                users[username] = password
    except FileNotFoundError:
        pass

# Save registered users to a file
def save_user(username, password):
    """
    Save a new user's username and password to a text file.
    @param username - the username of the new user
    @param password - the password of the new user
    """
    with open('users.txt', 'a') as file: # open the users.txt file in append mode
        # Write the username and password to the file in the format "username,password".
        file.write(f"{username},{password}\n")

# Broadcast a message to all online users
def broadcast(message, exclude=None):
    """
    Define a function to broadcast a message to all users except for the one specified in the 
    'exclude' parameter.
    @param message - The message to be broadcasted.
    @param exclude - The user to be excluded from receiving the message. Default is None.
    """
    # Iterate through online clients and send a message to each client except the one specified to 
    # exclude. If there is an exception during sending the message, it is caught and ignored.
    for user, client in online_clients.items():
        if user != exclude:
            try:
                # Send a message to the client after encoding it in UTF-8 format.
                client.send(message.encode('utf-8'))
            except:
                pass

# Handle individual client connections
def handle_client(client_socket, addr):
    """
    This function is intended to handle client connections.
    @param client_socket - the socket object for the client connection
    @param addr - the address of the client
    This function can be further implemented to define the actions to be taken when a client connects
    """
    username = None # Initialize a variable `username` with a value of `None`.
    try:
        # The server continuously listens for incoming data from client sockets and processes the 
        # commands accordingly.
        while True:
            # Receive data from a client socket with a buffer size of 1024 bytes and decode it using
            # UTF-8 encoding.
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            command, *args = data.split() # Split the input data into a command and its arguments.

            if command == "REGISTER":
                """
                Check if the command is "REGISTER" and process the registration of a new user.
                @param command - the command to be executed
                @param args - the arguments for the command
                @param client_socket - the socket for communication with the client
                @param users - the dictionary of existing users
                @return None
                """
                if len(args) != 2:
                    client_socket.send("Error: Invalid command format. Use REGISTER <username> <password>.".encode('utf-8'))
                    continue
                username, password = args
                if username in users:
                    client_socket.send("Error: Username already exists.".encode('utf-8'))
                else:
                    users[username] = password
                    save_user(username, password)
                    client_socket.send("Registration successful.".encode('utf-8'))

            elif command == "LOGIN":
                """
                Handle the "LOGIN" command. If the command format is invalid, send an error 
                message to the client. 
                Check if the username and password match the stored values. If the username is not 
                found or the password is incorrect, send an error message. If the username is already 
                logged in, send an error message. Otherwise, mark the user as online, notify other 
                clients about the login, and send a success message to the client.
                """
                if len(args) != 2:
                    client_socket.send("Error: Invalid command format. Use LOGIN <username> <password>.".encode('utf-8'))
                    continue
                username, password = args
                if username not in users or users[username] != password:
                    client_socket.send("Error: Invalid username or password.".encode('utf-8'))
                elif username in online_clients:
                    client_socket.send("Error: User already logged in.".encode('utf-8'))
                else:
                    online_clients[username] = client_socket
                    broadcast(f"{username} has joined the chat.", exclude=username)
                    client_socket.send("Login successful.".encode('utf-8'))

            elif command == "LIST_ONLINE":
                # Send a list of online users to the client socket when the command "LIST_ONLINE" is received.
                online_users = ', '.join(online_clients.keys())
                client_socket.send(f"Online users: {online_users}".encode('utf-8'))

            elif command == "SEND":
                """
                Handle the "SEND" command in a chat application.
                - If the user is not logged in, send an error message.
                - If the command format is invalid, send an error message.
                - Extract the recipient and message from the command arguments.
                - If the recipient is online, send the message to the recipient.
                - If the recipient is not online, send an error message.
                """
                if username is None:
                    client_socket.send("Error: Please login first.".encode('utf-8'))
                    continue
                if len(args) < 2:
                    client_socket.send("Error: Invalid command format. Use SEND <username> <message>.".encode('utf-8'))
                    continue
                recipient, message = args[0], ' '.join(args[1:])
                if recipient in online_clients:
                    online_clients[recipient].send(f"{username}: {message}".encode('utf-8'))
                else:
                    client_socket.send("Error: User is not online.".encode('utf-8'))

            elif command == "LOGOUT":
                """
                Check if the command is "LOGOUT" and if the username is in the list of online clients. 
                If so, remove the username from the online clients list and broadcast a message that the 
                user has left the chat. Then exit the loop.
                """
                if username in online_clients:
                    del online_clients[username]
                    broadcast(f"{username} has left the chat.")
                break

            else: # Send an error message to the client socket if an unknown command is received.
                client_socket.send("Error: Unknown command.".encode('utf-8'))
    except:
        pass
    finally: # perform cleanup actions when a client disconnects from the chat.
        if username in online_clients:
            del online_clients[username]
            broadcast(f"{username} has left the chat.")
        client_socket.close()

def handle_shutdown(signal, frame):
    """
    Handle the shutdown of the server by printing a message, closing the server, and exiting the program.
    @param signal - the signal to trigger the shutdown
    @param frame - the frame to handle the shutdown
    """
    print("\nShutting down server...")
    server.close()
    sys.exit(0)

# Register the signal handler for the SIGINT signal (Ctrl+C) to call the handle_shutdown function.
signal.signal(signal.SIGINT, handle_shutdown) 


# Start the server
def start_server():
    """
    Start server that listens for incoming connections, handles clients in separate threads, 
    and stops when an OSError occurs.
    """
    load_users()
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print("Server is running... Press Ctrl+C to stop.")

    while True:
        try:
            client_socket, addr = server.accept()
            print(f"Connection from {addr}")
            threading.Thread(target=handle_client, args=(client_socket, addr)).start()
        except OSError:
            break  # Break out of loop when server is closed
    
start_server()

