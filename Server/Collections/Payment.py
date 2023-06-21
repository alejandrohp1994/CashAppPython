import bson.objectid as oid

class PaymentTransactions:
    def __init__(self, database: object) -> None:
        self._collection = database["payment_transactions"]
        self._keys = ["userIdFrom", "userIdTo", "amount", "submittedBy", "notes"]
    
    @property
    def paymentId(self) -> str:
        return str(oid.ObjectId())
    
    def _verifyKeys(self, dictionary: dict) -> bool:
        """Verifies that the dictionary has the correct keys."""
        for key in self._keys:
            if key not in dictionary:
                return False
        return True
    
    def _logTransaction(self, dictionary: dict) -> bool and dict:
        """Logs the payment."""
        if not self._verifyKeys(dictionary):
            return False, {}
        
        dictionary["_id"] = self.paymentId
        response = self._collection.insert_one(dictionary)
        
        if not response.acknowledged:
            return False, {}
        
        return response.acknowledged, dictionary
    
    def createPayment(self, dictionary: dict) -> bool and dict:
        """Creates a payment."""
        status, document = self._logTransaction(dictionary)
        if not status:
            return False, {}
        return True, document
    
    def getAllPaymentsfromUser(self, userId: str) -> list:
        """Returns all payments from a user."""
        return list(self._collection.find({"userIdFrom": userId}))
    
    def getAllPaymentsToUser(self, userId: str) -> list:
        """Returns all payments to a user."""
        return list(self._collection.find({"userIdTo": userId}))

    def getAllPaymentsUserIsInvolvedIn(self, userId: str) -> list:
        """Returns all payments a user is involved in."""
        return list(self._collection.find(
            {"$or": [
                {"userIdFrom": userId}, 
                {"userIdTo": userId}
                ]
            }))

    def getPayment(self, paymentId: str) -> dict:
        """Returns a payment."""
        result = self._collection.find_one({"_id": paymentId})
        if result is None:
            return {}
        return dict(result)
    
    def deletePayment(self, paymentId: str) -> bool:
        """Deletes a payment."""
        response = self._collection.delete_one({"_id": paymentId})
        return response.acknowledged
    