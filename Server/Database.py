from MongoDB import MongoDB

from Collections.Users import Users
from Collections.Balance import BalanceTransactions
from Collections.Payment import PaymentTransactions
from Collections.Payment_Status import Payment_Status
from Collections.FriendRequest import FriendRequest
from Collections.FriendRequest_Status import FriendRequest_Status


from Timeout import ClassFun as ClassFun

CLASS = "DATABASE"

class Database:
    def __init__(self):
        pass
    
    @ClassFun(CLASS, "CONNECT")
    def connect(self):
        self.mongodb = MongoDB()
        self.mongodb.startLocalConnection()
    
    @ClassFun(CLASS, "CLOSE")
    def close(self):
        self.mongodb.closeLocalConnection()

    @ClassFun(CLASS, "SET DATABASE")
    def setDatabase(self, databaseName: str):
        self.db = self.mongodb.getDatabase(databaseName)

    @ClassFun(CLASS, "SET COLLECTIONS")
    def setCollections(self):
        self.users = Users(self.db)
        self.balance = BalanceTransactions(self.db)
        self.payment = PaymentTransactions(self.db)
        self.paymentStatus = Payment_Status(self.db)
        self.friendRequest = FriendRequest(self.db)
        self.friendRequestStatus = FriendRequest_Status(self.db)

    @ClassFun(CLASS, "HANDLE REQUEST")
    def handleRequest(self, action: str, request: dict):

        if action == "sign in":
            status, response = self.users.signIn(
                username=request["username"],
                password=request["password"]
                )
            return status, response
        
        elif action == "sign up":
            status, response = self.users.signUp(dictionary=request)
            return status, response
        
        elif action == "update details":
            status, response = self.users.updateDetails(
                userId=request["userId"],
                dictionary=request
                )
            return status, response
        
        elif action == "balance deposit":
            status, response = self.balance.addBalance(dictionary=request)
            return status, response
        
        elif action == "balance withdraw":
            status, response = self.balance.withdrawBalance(dictionary=request)
            return status, response
            
        elif action == "send payment":
            #Create payment document
            status, response = self.payment.createPayment(dictionary=request)
            #If payment document creation fails, return status and response
            if not status:
                return status, response
            #Create payment status document
            status2, response2 = self.paymentStatus.createPaymentStatus(
                    response["_id"], "accepted")
            #If payment status document creation fails, delete payment document
            if not status2:
                self.payment.deletePayment(response["_id"])
                return status2, response2
            
            #If both payment and payment status documents are created, return
            response["status"] = "accepted"
            response["paymentStatusId"] = response2["_id"]
            response["timestamp"] = response2["timestamp"]
            return True, response
        
        elif action == "request payment":
            #Create payment document
            status, response = self.payment.createPayment(dictionary=request)
            #If payment document creation fails, return status and response
            if not status:
                return status, response
            #Create payment status document
            status2, response2 = self.paymentStatus.createPaymentStatus(
                    response["_id"], "pending")
            #If payment status document creation fails, delete payment document
            if not status2:
                self.payment.deletePayment(response["_id"])
                return status2, response2
            
            #If both payment and payment status documents are created, return
            response["status"] = "pending"
            response["paymentStatusId"] = response2["_id"]
            response["timestamp"] = response2["timestamp"]
            return True, response

        elif action == "accept payment":
            status, response = self.paymentStatus.createPaymentStatus(
                paymentId=request["paymentId"],
                status="accepted"
                )
            if not status:
                return status, response
            payment_document = self.payment.getPayment(request["paymentId"])
            payment_document["status"] = "accepted"
            payment_document["paymentStatusId"] = response["_id"]
            payment_document["timestamp"] = response["timestamp"]
            return True, payment_document

        elif action == "decline payment":
            status, response = self.paymentStatus.createPaymentStatus(
                paymentId=request["paymentId"],
                status="cancelled"
                )
            if not status:
                return status, response
            payment_document = self.payment.getPayment(request["paymentId"])
            payment_document["status"] = "declined"
            payment_document["paymentStatusId"] = response["_id"]
            payment_document["timestamp"] = response["timestamp"]
            return True, payment_document
        
        elif action == "send friend request":
            #Create friend request document
            status, response = self.friendRequest.createFriendRequest(dictionary=request)
            #If friend request document creation fails, return status and response
            if not status:
                return status, response
            #Create friend request status document
            status2, response2 = self.friendRequestStatus.createFriendRequestStatus(
                    response["_id"], "pending")
            #If friend request status document creation fails, delete friend request document
            if not status2:
                self.friendRequest.deleteFriendRequest(response["_id"])
                return status2, response2
            response["status"] = "pending"
            response["friendRequestStatusId"] = response2["_id"]
            response["timestamp"] = response2["timestamp"]
            return True, response
        
        elif action == "delete friend" or action == "decline friend request":
            #Create friend request status document
            status, response = self.friendRequestStatus.createFriendRequestStatus(
                    friendRequestId=request["friendRequestId"],
                    status="cancelled")
            #If friend request status document creation fails, return status and response
            if not status:
                return status, response
            #Get friend request document
            friend_request_document = self.friendRequest.getFriendRequestById(
                request["friendRequestId"])
            friend_request_document["status"] = "cancelled"
            friend_request_document["friendRequestStatusId"] = response["_id"]
            friend_request_document["timestamp"] = response["timestamp"]
            return True, friend_request_document
        
        elif action == "accept friend request":
            #Create friend request status document
            status, response = self.friendRequestStatus.createFriendRequestStatus(
                    friendRequestId=request["friendRequestId"],
                    status="accepted")
            #If friend request status document creation fails, return status and response
            if not status:
                return status, response
            #Get friend request document
            friend_request_document = self.friendRequest.getFriendRequestById(
                request["friendRequestId"])
            friend_request_document["status"] = "accepted"
            friend_request_document["friendRequestStatusId"] = response["_id"]
            friend_request_document["timestamp"] = response["timestamp"]
            return True, friend_request_document

        elif action == "get current balance":
            balance_list = self.balance.getAllTransactions(request["userId"])
            
            balanceAmount = [balance["amount"] 
                             if balance["action"] == "deposit"
                                else -balance["amount"]
                             for balance in balance_list]
            
            payment_list = self.payment.getAllPaymentsUserIsInvolvedIn(
                userId=request["userId"])
            
            for payment in payment_list:
                status = self.paymentStatus.getMostRecentPaymentStatus(
                    payment["_id"])
                if status["status"] == "accepted":
                    if payment["userIdFrom"] == request["userId"]:
                        balanceAmount.append(-payment["amount"])
                    else:
                        balanceAmount.append(payment["amount"])
            
            balanceAmount = sum(balanceAmount)
            return True, {"balanceAmount": balanceAmount}

        elif action == "get balance history":
            response = self.balance.getAllTransactions(request["userId"])
            return True, response
        
        elif action == "get payment history":
            response = self.payment.getAllPaymentsUserIsInvolvedIn(
                userId=request["userId"])
            for payment in response:
                
                status = self.paymentStatus.getMostRecentPaymentStatus(
                    payment["_id"])
                print(status)
                payment["status"] = status["status"]
                payment["timestamp"] = status["timestamp"]
            return True, response
        
        elif action == "get friend requests pending":
            response = []
            response_ = self.friendRequest.getAllFriendRequestsUserIsInvolvedIn(
                userId=request["userId"])
            for friend_request in response_:
                status = self.friendRequestStatus.getMostRecentFriendRequestStatus(
                    friend_request["_id"])
                if status["status"] == "pending":
                    response.append(friend_request)
            return True, response
        
        elif action == "get friends":
            response = []
            response_ = self.friendRequest.getAllFriendRequestsUserIsInvolvedIn(
                userId=request["userId"])
            for friend_request in response_:
                status = self.friendRequestStatus.getMostRecentFriendRequestStatus(
                    friend_request["_id"])
                if status["status"] == "accepted":
                    response.append(friend_request)
            return True, response
        else:
            return False, "Invalid action"
        