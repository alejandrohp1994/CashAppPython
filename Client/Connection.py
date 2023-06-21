import socket


import json


# Define the host and port for the server
HOST = 'localhost'
PORT = 12345

class Connection:
    def __init__(self) -> None:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        """Connects to the server."""

        self._socket.connect((HOST, PORT))
        print('Connected to server.')

    def close(self):
        """Closes the connection."""

        self._socket.close()
        print('Connection closed.')

    def send(self, action: str, requestBody: dict) -> dict:
        """Sends data from the client to the server"""
        
        request = {
            "action": action,
            "requestBody": requestBody
        }
        
        formatted_request = json.dumps(request, indent=4)
        print("SEND")
        print("request", formatted_request)

        data = json.dumps(request).encode("utf-8")
        self._socket.sendall(data)
        return 
    
    def receive(self):
        """Receives data from the server"""


        data = self._socket.recv(8192)
        if data:
            data_received = json.loads(data.decode("utf-8"))
            


            formatted_request = json.dumps(data_received["responseBody"], indent=4)
            print("RECEIVE")
            print("request", formatted_request)

            return data_received