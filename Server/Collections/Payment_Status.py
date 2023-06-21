import datetime
import bson.objectid as oid
from pymongo import DESCENDING

class Payment_Status:
    def __init__(self, database: object) -> None:
        self._collection = database["payment_transactions_status"]
    
    @property
    def timestamp(self) -> str:
        """Returns the current timestamp."""
        return str(datetime.datetime.now())
    
    @property
    def paymentStatusId(self) -> str:
        return str(oid.ObjectId())
    
    def _logTransaction(self, paymentId: str, status:str) -> bool and dict:
        """Logs the payment."""
        document = {
            "_id": self.paymentStatusId,
            "paymentId": paymentId,
            "status": status,
            "timestamp": self.timestamp
            }
        response = self._collection.insert_one(document)
        
        return response.acknowledged, document
    
    def _getAllTransactions(self, paymentId: str) -> list:
        """Returns all payments status associated with payment id. 
        Sorts by timestamp"""

        documents = list(self._collection.find(
            {"paymentId" : f"{paymentId}"}
            ).sort('timestamp', DESCENDING))
        return documents

    def createPaymentStatus(self, paymentId: str, status: str) -> bool and dict:
        """Creates a payment status."""

        status, document = self._logTransaction(paymentId, status)
        if not status:
            return False, {}
        return True, document
    
    def getAllPaymentStatus(self, paymentId: str) -> dict:
        """Returns all payment status associated with the payment id.
        Sort by timestamp"""

        documents = self._getAllTransactions(paymentId)
        return documents
    
    def getMostRecentPaymentStatus(self, paymentId: str) -> dict:
        """Returns the most recent payment status associated with the payment id."""
        
        documents = self._getAllTransactions(paymentId)
        return documents[0]
    
    def getMostRecentPaymentStatusByStatus(self, paymentId: str, status: str) -> dict:
        """Returns the most recent payment status associated with the payment id."""
        
        documents = self._getAllTransactions(paymentId)
        for document in documents:
            if document["status"] == status:
                return document
        return {}
    