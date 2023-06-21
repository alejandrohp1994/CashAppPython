from tabulate import tabulate

class Payment:
    def __init__(self, USER: object) -> None:
        self._user = USER
        self._paymentTransactions = []

    def update(self, newPaymentTransactions: list):
        """Updates the payment transactions of the user.
        The new payment transactions are passed as a list of dictionaries."""
    
        self.paymentTransactions = newPaymentTransactions

    @property
    def userId(self):
        try:
            return self._user._details.userId
        except AttributeError:
            print("User not logged in")
            return None
        
    @property
    def paymentTransactions(self):
        return self._paymentTransactions
    @paymentTransactions.setter
    def paymentTransactions(self, newPaymentTransactions: list):
        self._paymentTransactions = newPaymentTransactions
    
    @property
    #Payments that you sent and requested
    def yourPayments(self):
        payments = [transaction 
                    for transaction in self.paymentTransactions 
                    if transaction["submittedBy"] == self.userId
                    ]
        return payments
    
    @property
    #Requests that you received
    def yourPaymentRequests(self):
        payments = [transaction 
                    for transaction in self.paymentTransactions 
                    if transaction["submittedBy"] != self.userId
                    ]
        return payments
    
    @property
    #Requests that you received and are pending
    def pendingPaymentRequests(self):
        paymentRequests = self.yourPaymentRequests
        paymentRequests = [request 
                           for request in paymentRequests 
                           if request["status"] == "pending"
                           ]
        return paymentRequests
    
    @property
    #Transactions that you sent and were accepted
    def acceptedPaymentRequests(self):
        paymentRequests = self.yourPaymentRequests
        paymentRequests = [request 
                           for request in paymentRequests 
                           if request["status"] == "accepted"
                           ]
        return paymentRequests
    
    @property
    #Transactions Accepted
    def acceptedTransactions(self):
        transactions = self.yourPayments
        transactions = [transaction 
                        for transaction in transactions 
                        if transaction["status"] == "accepted"
                        ]
        return transactions
    
    @property
    #Transactions Pending
    def pendingTransactions(self):
        transactions = self.yourPayments
        transactions = [transaction 
                        for transaction in transactions 
                        if transaction["status"] == "pending"
                        ]
        return transactions

    @property
    #Transactions Cancelled
    def cancelledTransactions(self):
        transactions = self.yourPayments
        transactions = [transaction 
                        for transaction in transactions 
                        if transaction["status"] == "cancelled"
                        ]
        return transactions

    def generatePaymentRequest(
            self, 
            userIdFrom: str, 
            userIdTo: str, 
            amount: float, 
            submittedBy: str,
            notes: str,
            ) -> dict:
        request = {
            'userIdFrom': userIdFrom,
            'userIdTo': userIdTo,
            'amount': amount,
            'submittedBy': submittedBy,
            'notes': notes,
        }
        return request
    
    def createPayment(self, friends: list, currentBalance: float):

        friend = input("Who do you want to pay?: ")
        if friend not in friends:
            print("You are not friends with this person")
        else:
            amount = float(input("How much do you want to pay?: "))
            if amount <= 0:
                print("You cannot pay a zero or negative amount")
            elif amount > currentBalance:
                print("You cannot pay more than your balance")
            else:
                notes = input("Notes: ")
                request = self.generatePaymentRequest(
                    userIdFrom=self.userId,
                    userIdTo=friend,
                    amount=amount,
                    submittedBy=self.userId,
                    notes=notes,
                )
                return request
            return None
        return None
    
    def createPaymentRequest(self, friends: list):
        friend = input("Who do you want to request money from?: ")
        if friend not in friends:
            print("You are not friends with this person")
        else:
            amount = float(input("How much do you want to request?: "))
            if amount <= 0:
                print("You cannot request a zero or negative amount")
            else:
                notes = input("Notes: ")
                request = self.generatePaymentRequest(
                    userIdFrom=friend,
                    userIdTo=self.userId,
                    amount=amount,
                    submittedBy=self.userId,
                    notes=notes,
                )
                return request
            return None
        return None

    def acceptDeclinePaymentRequest(self, currentBalance: float):
        if len(self.pendingPaymentRequests) == 0:
            print("You do not have any pending payment requests")
            return None
        
        sortedList = sorted(
            self.pendingPaymentRequests,
            key=lambda x: x['timestamp'], 
            reverse=True
            )
        headers = sortedList[0].keys()
        table = [item.values() for item in sortedList]
        print(tabulate(table, headers=headers, showindex=True, tablefmt="grid"))

        transactionIndex = int(input("Enter the row number: "))
        transaction = sortedList[transactionIndex]
        transactionId = transaction["_id"]
        amount = transaction["amount"]
        
        if currentBalance < amount:
            print("You do not have enough money to accept this payment")
        else:
            response = input("Accept or Decline: ")
            
            if response == "Accept":
                request = {"paymentId": transactionId}
                return request, "accept"
            
            elif response == "Decline":
                request = {"paymentId": transactionId}
                return request, "decline"
            
            else:
                print("Invalid response")
            return None
        return None