import certifi

from PIL import Image
from pymongo import MongoClient


class MongoDB:
    def __init__(self) -> None:
        print("[MongoDB] Starting MongoDB...")
        self._local = False
        self._remote = False

    def startLocalConnection(self):
        if self._remote:
            raise ValueError("[MongoDB] ERROR: REMOTE connection already started.")
        
        self._connection = MongoClient("mongodb://DEFAULT_LOCAL_HOST:YOUR_PORT_NUMBER") # Default MongoDB port
        self._local = True
        print("[MongoDB] MongoDB started! Set to LOCAL")
        
    def startRemoteConnection(self):
        if self._local:
            raise ValueError("[MongoDB] ERROR: LOCAL connection already started.")
        
        ca = certifi.where()
        
        username = "" # YOUR USERNAME
        password = "" # YOUR PASSWORD
        

        cluster = "YOUR_MONGODB_CLUSTER.MORE_DETAILS.mongodb.net/" # YOUR MONGODB CLUSTER ON ATLAS
        additional = "?retryWrites=true&w=majority" # ADDITIONAL DETAILS
        uri = 'mongodb+srv://' + username + ':' + password + '@' + cluster + additional
        
        self._connection = MongoClient(uri, tlsCAFile=ca)
        print("[MongoDB] MongoDB started! Set to REMOTE")

    def getDatabase(self, databaseName: str):

        # Check if the database already exists
        if databaseName in self._connection.list_database_names():
            print(f"Database '{databaseName}' already exists.")
        else:
            # Create the database
            self._connection[databaseName]
            print(f"Database '{databaseName}' created.")

        # Return the database pointer
        return self._connection[databaseName]

    def getCollection(self, databaseName: str, collectionName: str):
        
        db = self.getDatabase(databaseName)

        # Check if the collection already exists in the database
        if collectionName in db.list_collection_names():
            print(f"Collection '{collectionName}' already exists in the database.")
        else:
            # Create the collection
            db.create_collection(collectionName)
            print(f"Collection '{collectionName}' created in the database.")

        # Return the collection pointer
        return db[collectionName]

    def closeLocalConnection(self):
        if not self._local:
            raise ValueError("[MongoDB] ERROR: LOCAL connection not started.")
        
        self._connection.close()
        self._local = False
        print("[MongoDB] LOCAL connection closed.")

    def closeRemoteConnection(self):
        if not self._remote:
            raise ValueError("[MongoDB] ERROR: REMOTE connection not started.")
        
        self._connection.close()
        self._remote = False
        print("[MongoDB] REMOTE connection closed.")