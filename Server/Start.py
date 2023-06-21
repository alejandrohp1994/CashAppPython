from Server import Server

if __name__ == "__main__":
    print("\n\n\n\n")
    server = Server()
    server.startDatabaseConnection()
    server.startServerConnection()