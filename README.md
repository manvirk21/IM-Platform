# **Instant Messaging (IM) Platform**

This document serves as a README and project overview for the Instant Messaging (IM) Platform, detailing its purpose, functionality, and how to use it. A PDF version of this document is also available for download.



## **Project Overview**

The Instant Messaging (IM) Platform is a basic networking project designed to demonstrate real-time communication between multiple users. By implementing fundamental networking concepts, protocols, and security mechanisms, the project allows users to interact in a client-server architecture.



### **Key Features**

* **Network Architecture**:  
  * Utilizes a client-server architecture.  
  * The server handles multiple client connections simultaneously.  
  * Communication is established using the TCP/IP protocol.  
* **User Authentication**:  
  * New users can register with a unique username and password.  
  * Existing users can log in securely.  
  * The server maintains user information in a text file (`users.txt`).  
* **Online Clients**:  
  * Users can view a list of currently online clients.  
  * Real-time notifications when users join or leave the chat.  
* **Messaging**:  
  * Users can send private messages to others.  
  * Server handles message delivery and provides error messages for invalid operations.



## **File Overview**

* **server.py**: Contains the server-side code, which:  
  * Manages user registration, login, and logout.  
  * Broadcasts messages and maintains a list of online users.  
  * Handles commands from clients (e.g., REGISTER, LOGIN, LOGOUT).  
* **client.py**: Contains the client-side code, which:  
  * Connects to the server and allows users to input commands.  
  * Handles sending and receiving messages asynchronously.



## **Installation and Usage**

### **Prerequisites**

* Python 3.x

### **Setup Instructions**

1. Clone or download the project files.  
2. Ensure Python 3.x is installed on your system.  
3. Open a terminal and navigate to the project directory.

### **Running the Server**

1. Execute the following command to start the server:  
   python server.py  
2. The server listens on `127.0.0.1` (localhost) and port `5001`.  
3. Press `Ctrl+C` to stop the server (once you are finished).

### **Running the Client**

1. Execute the following command to start a client:  
   python client.py  
2. Enter commands as prompted to register, log in, or interact with other users.

### **Commands**

* `REGISTER <username> <password>`: Register a new account.  
* `LOGIN <username> <password>`: Log in to your account.  
* `LIST_ONLINE`: View a list of currently online users.  
* `SEND <username> <message>`: Send a private message to a user.  
* `LOGOUT`: Log out of your account.



## **Example Workflow**

1. Start the server (`server.py`) on one terminal.  
2. Start one or more clients (`client.py`) on separate terminals.  
3. Clients register using the `REGISTER` command.  
4. Clients log in using the `LOGIN` command.  
5. Use `LIST_ONLINE` to see other online users.  
6. Send messages to others using the `SEND` command.  
7. Log out using the `LOGOUT` command.



## **Notes and Limitations**

* The server is designed for local testing on `127.0.0.1`. For network-wide communication, update the `HOST` variable.  
* Error handling is basic and requires enhancement for other uses beyond this project.  
* Messages are not encrypted and should not be used in sensitive environments.



## **Future Improvements**

* Encrypt communications using SSL/TLS.  
* Implement group chat functionality.  
* Add a graphical user interface (GUI).

