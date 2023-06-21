import bson.objectid as oid

class FriendRequest:
    def __init__(self, database: object) -> None:
        self._collection = database["friend_requests"]
        self._keys = ["userIdFrom", "userIdTo"]

    @property
    def friendRequestId(self) -> str:
        return str(oid.ObjectId())
    
    def _verifyKeys(self, dictionary: dict) -> bool:
        """Verifies that the dictionary has the correct keys."""
        for key in self._keys:
            if key not in dictionary:
                return False
        return True
    
    def _logFriendRequest(self, dictionary: dict) -> bool and dict:
        """Logs the friend request."""
        if not self._verifyKeys(dictionary):
            return False, {}
        
        dictionary["_id"] = self.friendRequestId
        response = self._collection.insert_one(dictionary)

        return response.acknowledged, dictionary
    
    def createFriendRequest(self, dictionary: dict) -> bool and dict:
        """Creates a friend request."""
        status, document = self._logFriendRequest(dictionary)
        if not status:
            return False, {}
        return True, document
    
    def getAllFriendRequestsReceived(self, userId: str) -> list:
        """Returns all friend requests associated with the user."""
        return list(self._collection.find({"userIdTo": userId}))
    
    def getAllFriendRequestsSent(self, userId: str) -> list:
        """Returns all friend requests sent by the user."""
        return list(self._collection.find({"userIdFrom": userId}))

    def getAllFriendRequestsUserIsInvolvedIn(self, userId: str) -> list:
        """Returns all payments a user is involved in."""
        return list(self._collection.find(
            {"$or": [
                {"userIdFrom": userId}, 
                {"userIdTo": userId}
                ]
            }))

    def getFriendRequestById(self, friendRequestId: str) -> dict:
        """Returns a friend request."""
        result =  self._collection.find_one({"_id": friendRequestId})
        if result is None:
            return {}
        return result
    
    def deleteFriendRequest(self, friendRequestId: str) -> bool:
        """Deletes a friend request."""
        response = self._collection.delete_one({"_id": friendRequestId})
        return response.acknowledged