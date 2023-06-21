

class AppClientSide:
    def __init__(self, USER: object) -> None:
        self.USER = USER

        self.SIGN_IN_SIGN_UP = [
            "Welcome to CashApp!",
            "1. Sign Up",
            "2. Sign In",
            "3. Exit"
        ]

        self.MAIN_MENU = [
            "Main Menu",
            "1. Details",
            "2. Balance",
            "3. Payment",
            "4. Friends",
            "5. Exit"
        ]

        self.DETAILS_MENU = [
            "Details",
            "1. Update Details",
            "2. View Details",
            "3. Exit"
        ]

        self.BALANCE_MENU = [
            "Balance",
            "1. Add Balance",
            "2. Withdraw Balance",
            "3. View Balance",
            "4. Exit"
        ]

        self.PAYMENT_MENU = [
            "Payment",
            "1. Send Payment",
            "2. Request Payment",
            "3. Accept/Deny Requests",
            "4. View Payment/Request History",
            "5. View Completed Transactions",
            "6. View Pending Transactions",
            "7. View Cancelled Transactions",
            "8. Exit"
        ]

        self.FRIENDS_MENU = [
            "Friends",
            "1. Add Friend",
            "2. Remove Friend",
            "3. Accept/Deny Friend Request",
            "4. View Friends",
            "5. View Pending Friend Requests",
            "6. Exit"
        ]

    def printOptions(self, options: list):
        print("\n")
        for row in options:
            print(row)
        option = int(input("Enter your option: "))
        return option
    
    def start(self):
        option = self.printOptions(self.SIGN_IN_SIGN_UP)
        print("\n")

        if option == 1:
            status = self.USER.signUp()
            if status == True:
                self.mainMenu()
            else:
                print("Error: Could not sign up.")
        elif option == 2:
            status = self.USER.signIn()
            if status == True:
                self.mainMenu()
            else:
                print("Error: Could not sign in.")
        elif option == 3:
            #EXIT PROGRAM
            print("Exiting...")
            exit()
        else:
            print("Invalid option.")
            self.start()


    def mainMenu(self):
        option = self.printOptions(self.MAIN_MENU)
        print("\n")

        if option == 1:
            self.detailsMenu()
        elif option == 2:
            self.balanceMenu()
        elif option == 3:
            self.paymentMenu()
        elif option == 4:
            self.friendsMenu()
        elif option == 5:
            self.USER.signOut()
            #EXIT PROGRAM
            print("Exiting...")
            exit()
        else:
            print("Invalid option.")
            self.mainMenu()

    def detailsMenu(self):
        option = self.printOptions(self.DETAILS_MENU)
        print("\n")

        if option == 1:
            self.USER.updateDetails()
        elif option == 2:
            self.USER.viewDetails()
        elif option == 3:
            self.mainMenu()
        else:
            print("Invalid option.")
            self.detailsMenu()
        self.mainMenu()

    def balanceMenu(self):
        option = self.printOptions(self.BALANCE_MENU)
        print("\n")

        if option == 1:
            self.USER.addBalance()
        elif option == 2:
            self.USER.withdrawBalance()
        elif option == 3:
            self.USER.viewBalance()
        elif option == 4:
            self.mainMenu()
        else:
            print("Invalid option.")
            self.balanceMenu()
        self.mainMenu()


    def paymentMenu(self):
        option = self.printOptions(self.PAYMENT_MENU)
        print("\n")

        if option == 1:
            self.USER.sendPayment()
        elif option == 2:
            self.USER.requestPayment()
        elif option == 3:
            self.USER.acceptDenyRequests()
        elif option == 4:
            self.USER.viewPaymentRequestHistory()
        elif option == 5:
            self.USER.viewCompletedTransactions()
        elif option == 6:
            self.USER.viewPendingTransactions()
        elif option == 7:
            self.USER.viewCancelledTransactions()
        elif option == 8:
            self.mainMenu()
        else:
            print("Invalid option.")
            self.paymentMenu()
        self.mainMenu()


    def friendsMenu(self):
        option = self.printOptions(self.FRIENDS_MENU)
        print("\n")

        if option == 1:
            request = self.USER.addFriend()
        elif option == 2:
            request = self.USER.removeFriend()
        elif option == 3:
            request = self.USER.acceptDenyFriendRequest()
        elif option == 4:
            self.USER.viewFriends()
        elif option == 5:
            self.USER.viewPendingFriendRequests()
        elif option == 6:
            self.mainMenu()
        else:
            print("Invalid option.")
            self.friendsMenu()
        self.mainMenu()


