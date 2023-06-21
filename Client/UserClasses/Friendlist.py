from tabulate import tabulate

class Friendlist:
    def __init__(self, USER: object) -> None:
        self._user = USER
        self._friendsPending = []
        self._friendsAccepted = []

    def updateAccepted(self, newFriends: list):
        """Updates the accepted friends of the user.
        The new friends are passed as a list of dictionaries."""
        
        self._friendsAccepted = newFriends

    def updatePending(self, newFriends: list):
        """Updates the pending friends of the user.
        The new friends are passed as a list of dictionaries."""
        
        self._friendsPending = newFriends

    @property
    def friendsAccepted(self):
        return self._friendsAccepted
    @friendsAccepted.setter
    def friendsAccepted(self, newFriends: list):
        self._friendsAccepted = newFriends

    @property
    def friendsPending(self):
        return self._friendsPending
    @friendsPending.setter
    def friendsPending(self, newFriends: list):
        self._friendsPending = newFriends

    @property
    def userId(self):
        try:
            return self._user._details.userId
        except AttributeError:
            print("User not logged in")
            return None

    @property
    def acceptedFriendsByUsername(self) -> list:
        friends = [
            friend["userIdTo"] if friend["userIdFrom"] == self.userId 
            else friend["userIdFrom"]
            for friend in self.friendsAccepted]
        return friends

    @property
    def pendingFriendsByUsername(self) -> list:
        friends = [
            friend["userIdTo"] if friend["userIdFrom"] == self.userId 
            else friend["userIdFrom"]
            for friend in self.friendsPending]
        return friends

    @property
    def pendingFriendsIncoming(self) -> list:
        friends = [friend
                   for friend in self.friendsPending
                   if friend["userIdTo"] == self.userId]
        return friends

    @property
    def pendingFriendsOutgoing(self) -> list:
        friends = [friend
                   for friend in self.friendsPending
                   if friend["userIdFrom"] == self.userId]
        return friends

    def addFriend(self):
        friendUserame = input("Who do you want to add as a friend?: ")
        
        if friendUserame == self.userId:
            print("You cannot send a friend request to yourself.")
            return None
        if friendUserame in self.acceptedFriendsByUsername:
            print("You are already friends with this user.")
            return None
        if friendUserame in self.pendingFriendsByUsername:
            print("You have already sent or received a friend request to this user.")
            return None
        else:
            request = {
                "userIdFrom": self.userId,
                "userIdTo": friendUserame
            }
            return request
    
    def acceptDeclineFriendRequest(self):
        table = self.pendingFriendsIncoming
        print(tabulate(
            table, 
            headers=table[0].keys(), 
            showindex=True,
            tablefmt="grid"))
        friendIndex = int(input("Which friend do you want to accept or decline? (Put the row number): "))
        friend = self.pendingFriendsIncoming[friendIndex]
        response = input("Accept or Decline?: ")
        if response == "Accept":
            request = {"friendRequestId": friend["_id"]}
            return request, "accept"
        elif response == "Decline":
            request = {"friendRequestId": friend["_id"]}
            return request, "decline"
        else:
            print("Invalid response")
            return None
    
    def deleteFriend(self):
        table = self.friendsAccepted
        print(tabulate(
            table, 
            headers=table[0].keys(), 
            showindex=True,
            tablefmt="grid"))
        friendIndex = int(input("Which friend do you want to delete? (Put the row number): "))
        friend = self.friendsAccepted[friendIndex]
        request = {
                "friendRequestId": friend["_id"],
                "status": "cancelled"
        }
        return request