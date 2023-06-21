from tabulate import tabulate

from UserClasses.UserBalance import Balance
from UserClasses.Details import Details
from UserClasses.Friendlist import Friendlist
from UserClasses.UserPayment import Payment

import Connection

class User:
    def __init__(self):
        self._details = Details()
        self._friendlist = Friendlist(self)
        self._balance = Balance(self)
        self._payment = Payment(self)

        self._connection = Connection.Connection()

    def startConnection(self):
        print("Starting connection...")
        self._connection.connect()

    def closeConnection(self):
        print("Closing connection...")
        self._connection.close()



    def getCurrentBalance(self):
        requestBody = { "userId": self._details.userId }
        self._connection.send("get current balance", requestBody)
        response = self._connection.receive()
        if not response["status"]:
            return False
        self._details.balance = float(response["responseBody"]["balanceAmount"])
        return True
    
    def getBalanceHistory(self):
        requestBody = { "userId": self._details.userId }
        self._connection.send("get balance history", requestBody)
        response = self._connection.receive()
        if not response["status"]:
            return False
        self._balance.update(response["responseBody"])
        return True
    
    def getPaymentHistory(self):
        requestBody = { "userId": self._details.userId }
        self._connection.send("get payment history", requestBody)
        response = self._connection.receive()
        if not response["status"]:
            return False
        self._payment.update(response["responseBody"])
        return True
    
    def getFriendRequestsPending(self):
        requestBody = { "userId": self._details.userId }
        self._connection.send("get friend requests pending", requestBody)
        response = self._connection.receive()
        if not response["status"]:
            return False
        self._friendlist.updatePending(response["responseBody"])
        return True
    
    def getFriends(self):
        requestBody = { "userId": self._details.userId }
        self._connection.send("get friends", requestBody)
        response = self._connection.receive()
        if not response["status"]:
            return False
        self._friendlist.updateAccepted(response["responseBody"])
        return True
    
    #MAIN MENU OPTION 1
    #Sign Up
    def updateDetails(self):
        print("SIGN UP")
        requestBody = self._details.signUp()
        
        self.startConnection()

        self._connection.send("sign up", requestBody)
        response = self._connection.receive()
        
        if not response["status"]:
            return False
        
        self._details.create(response["responseBody"])
        return True

    #MAIN MENU OPTION 2
    #Sign In
    def signIn(self):
        print("SIGN IN")
        requestBody = self._details.signIn()

        self.startConnection()

        self._connection.send("sign in", requestBody)
        response = self._connection.receive()
        print(response)
        if not response["status"]:
            return False
        
        #Populate user details
        self._details.create(response["responseBody"])
        #Get user current balance
        self.getCurrentBalance()
        #Get user balance history
        self.getBalanceHistory()
        #Get user payment history
        self.getPaymentHistory()
        #Get user friends
        self.getFriends()
        #Get user friend requests pending
        self.getFriendRequestsPending()
        return True

    def signOut(self):
        print("SIGN OUT")
        requestBody = { "userId": self._details.userId }
        self._connection.send("sign out", requestBody)
        response = self._connection.receive()
        
        if not response["status"]:
            return False    
        
        self._connection.close()
        return True

    #DETAILS: OPTION 1
    #Update Details
    def updateDetails(self):
        print("UPDATE DETAILS")
        requestBody = self._details.createRequestToUpdate()
        if requestBody == None:
            return None
        
        self._connection.send("update details", requestBody)
        response = self._connection.receive()
        
        if not response["status"]:
            return False    
        
        self._details.update(response["responseBody"])
        return True

    #DETAILS: OPTION 2
    #View Details
    def viewDetails(self):
        print("VIEW DETAILS")
        table = self._details.viewDetails()
        print(tabulate(table, tablefmt="grid"))

    #BALANCE: OPTION 1
    #Deposit Balance
    def depositBalance(self):
        print("ADD TO BALANCE")
        requestBody = self._balance.createDepositRequest()
        if requestBody == None:
            return None
        
        self._connection.send("balance deposit", requestBody)
        response = self._connection.receive()

        if not response["status"]:
            return False
        self._balance.update(response["responseBody"])
        self.getCurrentBalance()
        return True

    #BALANCE: OPTION 2
    def withdrawBalance(self):
        print("WITHDRAW FROM BALANCE")
        requestBody = self._balance.createWithdrawRequest(self.currentBalance)
        if requestBody == None:
            return None
        
        self._connection.send("balance withdraw", requestBody)
        response = self._connection.receive()
        
        if not response["status"]:
            return False    
        self._balance.update(response["responseBody"])
        self.getCurrentBalance()
        return True

    #BALANCE: OPTION 3
    #View Balance
    def viewBalance(self):
        print("VIEW BALANCE")
        table = [["Current Balance", str(self._details.balance)]]
        print(tabulate(table, tablefmt="grid"))
    

    #PAYMENT: OPTION 1
    #Send Payment
    def sendPayment(self):
        print("SEND PAYMENT")
        requestBody = self._payment.createPayment(
            self._friendlist.acceptedFriendsByUsername,
            self.currentBalance
            )
        if requestBody == None:
            return None
        self._connection.send("send payment", requestBody)
        response = self._connection.receive()
        
        if not response["status"]:
            return False
        
        self._payment.update(response["responseBody"])
        self.getCurrentBalance()
        return True


    #PAYMENT: OPTION 2
    #Request Payment
    def requestPayment(self):
        print("REQUEST PAYMENT")
        requestBody = self._payment.createPaymentRequest(
            self._friendlist.acceptedFriendsByUsername
            )
        if requestBody == None:
            return None
        
        self._connection.send("request payment", requestBody)
        response = self._connection.receive()
        
        if not response["status"]:
            return False
        
        self._payment.update(response["responseBody"])
        return True

    
    #PAYMENT: OPTION 3
    #Accept/Deny Request
    def acceptDeclineRequest(self):
        print("ACCEPT/DENY REQUEST")
        requestBody, decision = self._payment.createAcceptDeclineRequest(
            self.currentBalance)
        if requestBody == None:
            return None
        
        self._connection.send(f"{decision} request", requestBody)
        response = self._connection.receive()
        
        if not response["status"]:
            return False
        
        self._payment.update(response["responseBody"])
        return True
        

    #PAYMENT: OPTION 4
    #View Payment History
    def viewPaymentRequestHistory(self):
        print("VIEW PAYMENT/REQUEST HISTORY")
        table = self._payment.paymentTransactions
        if table == None or table == []:
            print("No details to display")
        else:
            print(tabulate(table, headers="keys", tablefmt="grid"))

    #PAYMENT: OPTION 5
    #View Completed Transactions
    def viewCompletedTransactions(self):
        print("VIEW COMPLETED TRANSACTIONS")
        table = self._payment.acceptedTransactions
        if table == None or table == []:
            print("No details to display")
        else:
            print(tabulate(table, headers="keys", tablefmt="grid"))
    
    #PAYMENT: OPTION 6
    #View Pending Transactions
    def viewPendingTransactions(self):
        print("VIEW PENDING TRANSACTIONS")
        table = self._payment.pendingTransactions
        if table == None or table == []:
            print("No details to display")
        else:
            print(tabulate(table, headers="keys", tablefmt="grid"))

    #PAYMENT: OPTION 7
    #View Cancelled Transactions
    def viewCancelledTransactions(self):
        print("VIEW CANCELLED TRANSACTIONS")
        table = self._payment.cancelledTransactions
        if table == None or table == []:
            print("No details to display")
        else:
            print(tabulate(table, headers="keys", tablefmt="grid"))

    #FRIENDS: OPTION 1
    #Add Friend
    def addFriend(self):
        print("SEND FRIEND REQUEST")
        requestBody = self._friendlist.addFriend()
        if requestBody == None:
            return None
        
        self._connection.send("send friend request", requestBody)
        response = self._connection.receive()
        
        if not response["status"]:
            return False
        
        self._payment.update(response["responseBody"])
        return True

    #FRIENDS: OPTION 2
    #Remove Friend
    def deleteFriend(self):
        print("DELETE FRIEND")
        requestBody = self._friendlist.deleteFriend()
        if requestBody == None:
            return None
        
        self._connection.send("delete friend", requestBody)
        response = self._connection.receive()
        
        if not response["status"]:
            return False
        
        self._payment.update(response["responseBody"])
        return True

    #FRIENDS: OPTION 3
    #Accept/Deny Friend Request
    def acceptDenyFriendRequest(self):
        print("ACCEPT/DENY FRIEND REQUEST")
        requestBody, decision = self._friendlist.acceptDeclineFriendRequest()
        if requestBody == None:
            return None
        
        self._connection.send(f"{decision} friend request", requestBody)
        response = self._connection.receive()
        
        if not response["status"]:
            return False
        
        self._payment.update(response["responseBody"])
        return True

    #FRIENDS: OPTION 4
    #View Friends
    def viewFriends(self):
        print("VIEW FRIENDS")
        table = self._friendlist.acceptedFriendsByUsername
        if table == None or table == []:    
            print("No details to display")
        else:
            formatted_table = [[username] for username in table]
            print(tabulate(formatted_table, headers= ["Username"], tablefmt="plain"))

    #FRIENDS: OPTION 5
    #View Pending Friend Requests
    def viewPendingFriendRequests(self):
        print("VIEW PENDING FRIEND REQUESTS")
        table = self._friendlist.pendingFriendsByUsername
        if table == None or table == []:
            print("No details to display")
        else:
            formatted_table = [[username] for username in table]
            print(tabulate(formatted_table, headers= ["Username"], tablefmt="plain"))
