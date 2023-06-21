import datetime
import bson.objectid as oid

class BalanceTransactions:
    def __init__(self, database: object) -> None:
        self._collection = database["balance_transactions"]

    @property
    def timestamp(self) -> str:
        """Returns the current timestamp."""
        return str(datetime.datetime.now())
    
    @property
    def balanceId(self) -> str:
        return str(oid.ObjectId())


    def _verifyKeys(self, dictionary: dict) -> bool:
        """Verifies that the dictionary has the correct keys."""
        return "userId" in dictionary and "amount" in dictionary


    def _logTransaction(self, action: str, userId: str, amount: float) -> bool and dict:
        document = {
            "_id": self.balanceId,
            "userId": userId,
            "action": action,
            "amount": amount,
            "timestamp": self.timestamp
        }
        
        response = self._collection.insert_one(document)
        if not response.acknowledged:
            return False, {}
        return True, document

    def addbalance(self, dictionary: dict) -> bool and dict:
        """Adds balance to the user."""
        if not self._verifyKeys(dictionary):
            return False, {}
        
        status, document = self._logTransaction(
            "deposit", 
            dictionary["userId"], 
            dictionary["amount"]
            )
        if not status:
            return False, {}
        
        return status, document
    
    def withdrawBalance(self, dictionary: dict) -> bool and dict:
        """Withdraws balance from the user."""
        if not self._verifyKeys(dictionary):
            return False, {}
        
        status, document = self._logTransaction(
            "withdraw", 
            dictionary["userId"], 
            dictionary["amount"]
            )
        if not status:
            return False, {}
        
        return status, document
    
    def getAllTransactions(self, username: str) -> list:
        """Returns all the transactions for the user."""
        transactions = list(self._collection.find({"userId": username}))
        return transactions
    
    def getTransaction(self, transactionId: str) -> dict:
        """Returns the transaction for the transactionId."""
        transaction = self._collection.find_one({"_id": transactionId})
        if transaction is None:
            return {}
        return dict(transaction)
