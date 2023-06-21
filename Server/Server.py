
from Database import Database
from Connection import Connection

from Timeout import ClassFun as ClassFun


HOST = 'localhost'
PORT = 12345

DATABASE_NAME = "CashApp"


CLASS = "SERVER"

class Server:
    def __init__(self):
        pass

    def startDatabaseConnection(self):
        """Starts the database."""
        self._database = Database()
        self._database.connect()
        self._database.setDatabase(DATABASE_NAME)
        self._database.setCollections()

    def startServerConnection(self):
        self._connection = Connection(self)
        self._connection.start(HOST, PORT)
        self._connection.run()
    
    @ClassFun(CLASS, "HANDLE REQUEST")
    def handleRequest(self, action: str, request: dict):
        status, result = self._database.handleRequest(action, request)
        return status, result
    

    def close(self):
        self._connection.close()
        self._database.close()

