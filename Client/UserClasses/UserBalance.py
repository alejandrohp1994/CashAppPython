class Balance:
    def __init__(self, USER: object) -> None:
        self._user = USER
        self._balanceTransactions = []

    def update(self, newBalanceTransactions: list):
        """Updates the balance transactions of the user.
        The new balance transactions are passed as a list of dictionaries."""
    
        self.balanceTransactions = newBalanceTransactions

    @property
    def userId(self):
        try:
            return self._user._details.userId
        except AttributeError:
            print("User not logged in")
            return None
    
    @property
    def balanceTransactions(self):
        return self._balanceTransactions
    @balanceTransactions.setter
    def balanceTransactions(self, newBalanceTransactions: list):
        balanceTransactions = newBalanceTransactions
        # Sort the list of dictionaries by the timestamp
        self._balanceTransactions = sorted(
            balanceTransactions, 
            key=lambda x: x['timestamp'],
            reverse=True
            )

    def generateBalanceRequest(self, userId: str, action: str, amount: float) -> dict:
        return { 
            "userId": userId,
            "action": action,
            "amount": amount
            }
    
    def createDepositRequest(self):
        amount = float(input("Enter the amount you want to add to your balance: "))
        
        if amount <= 0:
            print("You cannot deposit a zero or negative amount")
            return None
        else:
            request = self.generateBalanceRequest(
                self.userId,
                "deposit",
                amount
                )
            return request

    def createWithdrawRequest(self, currentBalance: float):
        amount = float(input("Enter the amount you want to withdraw from your balance: "))
        
        if amount <= 0:
            print("You cannot withdraw a zero or negative amount")
        elif amount > currentBalance:
            print("You cannot withdraw more than your balance")
        else:
            request = self.generateBalanceRequest(
                self.userId,
                "withdraw",
                amount
                )
            return request
        return None
    
    def update(self, newBalanceTransactions: list):
        self.balanceTransactions = newBalanceTransactions