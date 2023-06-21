class Users:
    def __init__(self, database: object) -> None:
        self._collection = database["users"]
    
    def _logUser(self, dictionary: dict) -> bool and dict:
        response = self._collection.insert_one(dictionary)
        if response.acknowledged:
            return True, response
        else:
            return False, {}
        
    def _getUser(self, username: str) -> dict:
        user = self._collection.find_one({"username": username})
        if user != None:
            return True, dict(user)
        else:
            return False, {}
        
    def _checkUsernameExists(self, username: str) -> bool:
        #Used to check if username is taken for sign up
        #Used to check if user exists when sending friend request
        """Checks if the username exists in the database."""
        return self._collection.find_one({"username": username}) != None
    
    def signUp(self, dictionary: dict) -> bool and dict:
        """Creates a user in the database."""
        if not self._checkUsernameExists(dictionary["username"]):
            return self._logUser(dictionary)
        else:
            return False, {}
    
    def signIn(self, username: str, password: str) -> bool and dict:
        """Signs in the user and returns the responseBody. 
        If the user does not exist, returns an empty dictionary."""
        userExists, user = self._getUser(username)
        if userExists:
            if user["password"] == password:
                return True, user
            else:
                return False, {}
        else:
            return False, {}
        
    def updateDetails(self, username: str, dictionary: dict) -> bool and dict:
        """Updates the user details in the database."""
        userExists, user = self._getUser(username)
        if userExists:
            response = self._collection.update_one(
                {"username": username}, 
                {"$set": dictionary}
                )
            if response.acknowledged:
                return True, response
            else:
                return False, {}
        else:
            return False, {}