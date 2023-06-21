import datetime
import bson.objectid as oid
from pymongo import DESCENDING

class FriendRequest_Status:
    def __init__(self, database: object) -> None:
        self._collection = database["friend_requests_status"]
    
    @property
    def timestamp(self) -> str:
        """Returns the current timestamp."""
        return str(datetime.datetime.now())
    
    @property
    def friendRequestStatusId(self) -> str:
        return str(oid.ObjectId())
    
    def _logTransaction(self, friendRequestId: str, status:str) -> bool and dict:
        """Logs the payment."""
        document = {
            "_id": self.friendRequestStatusId,
            "friendRequestId": friendRequestId,
            "status": status,
            "timestamp": self.timestamp
            }
        response = self._collection.insert_one(document)
        
        return response.acknowledged, document
    
    def _getAllTransactions(self, friendRequestId: str) -> list:
        """Returns all payments associated with friend request id. 
        Sorts by timestamp"""

        documents = list(self._collection.find(
            {"friendRequestId" : f"{friendRequestId}"}
            ).sort('timestamp', DESCENDING))
        return documents

    def createFriendsRequestStatus(self, friendRequestId: str, status: str) -> bool and dict:
        """Creates a friend request status."""

        status, document = self._logTransaction(friendRequestId, status)
        if not status:
            return False, {}
        return True, document
    
    def getAllFriendRequestStatus(self, friendRequestId: str) -> dict:
        """Returns all friend request status associated with the payment id.
        Sort by timestamp"""

        documents = self._getAllTransactions(friendRequestId)
        return documents
    
    def getMostRecentFriendRequestStatus(self, friendRequestId: str) -> dict:
        """Returns the most recent payment status associated with the payment id."""
        
        documents = self._getAllTransactions(friendRequestId)
        return documents[0]