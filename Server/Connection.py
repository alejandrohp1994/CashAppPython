import socket
import json
import select

from Timeout import ClassFun as ClassFun

CLASS = "CONNECTION"

class Connection:
    def __init__(self, server: object):
        self._server = server
        
        # Create a socket object
        self._server_socket = None
        self._connections = []

    @property
    def server_socket(self):
        return self._socket

    @server_socket.setter
    def server_socket(self, value):
        self._socket = value

    @ClassFun(CLASS, "START")
    def start(self, host: str, port: int, max_connections: int = 5):
        """Starts server connections."""

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Bind the socket to the host and port
        self.server_socket.bind((host, port))

        # Set the maximum number of connections
        self.server_socket.listen(max_connections)
        
        # Allows the socket to be reused
        #self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        
        print('Server is waiting for connections...')

        self._connections.append(self.server_socket)


    def run(self):
        """Runs the server."""

        while True:
            try:
                read_sockets, _, exception_sockets = select.select(self._connections, [], self._connections)

                for notified_socket in read_sockets:
                    if notified_socket == self.server_socket:
                        self.addNewConnection()
                    else:
                        # Incoming message from an existing client
                        self.handleExistingClient(notified_socket)

                for notified_socket in exception_sockets:
                    self.closeClient(notified_socket)
            
            #KeyboardInterrupt is raised when the user presses Ctrl+c
            except KeyboardInterrupt:
                print("Server stopped.")
                break
        self.closeServer()
    

    @ClassFun(CLASS, "ADD NEW CONNECTION")
    def addNewConnection(self):
        # Accept a client connection
        client_socket, client_address = self.server_socket.accept()
        print('New Connection! Connected to:', client_address)
        self._connections.append(client_socket)


    @ClassFun(CLASS, "HANDLE EXISTING CLIENT")
    def handleExistingClient(self, client_socket: socket):
        """Handles client connections."""

        try:
            data = client_socket.recv(8192)
            if data:
                action, requestBody = self.receive(data)
                
                if action == "sign out":
                    self.send("signed out", {}, client_socket)
                    print(f"Client disconnected! {requestBody['username']} signed out.")
                    self.closeClient(client_socket)
                    return
                
                status, responseBody = self._server.handleRequest(action, requestBody)

                # Send a response
                self.send(status, responseBody, client_socket)

            else:
                # Empty data received, client disconnected
                print("Client disconnected! Connection closed by client.")
                self.closeClient(client_socket)

        except Exception as e:
            print("Error! handling connection:", str(e))
            self.closeClient(client_socket)


    @ClassFun(CLASS, "RECEIVE")
    def receive(self, data: bytes):
        """Receives a dictionary from the client and returns the action and requestBody."""
        print("Reading incoming data")
        

        received_dictionary = json.loads(data.decode("utf-8"))

        action = received_dictionary["action"]
        requestBody = received_dictionary["requestBody"]
        
        print("ACTION: ", action)
        print("REQUEST BODY: ", requestBody)
        
        return action, requestBody
    

    @ClassFun(CLASS, "SEND")
    def send(self, status: str, response: dict, client_socket: socket):
        """Sends data from the server to the client"""
        
        response = {
            "status": status,
            "responseBody": response
        }
        print("response", response)
        # Send a dictionary to the client
        data = json.dumps(response).encode("utf-8")
        client_socket.sendall(data)

    @ClassFun(CLASS, "CLOSE CLIENT")
    def closeClient(self, client_socket: socket):
        """Closes the client connection"""

        print("Client disconnected: ", client_socket.getpeername())
        self._connections.remove(client_socket)
        client_socket.close()

    @ClassFun(CLASS, "CLOSE SERVER")
    def closeServer(self):
        """Closes the server connection."""

        print("Server shutting down...")
        for client_socket in self._connections:
            if client_socket != self.server_socket:
                client_socket.close()
        self.server_socket.close()