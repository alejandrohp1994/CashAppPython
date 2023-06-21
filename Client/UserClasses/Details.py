class Details:
    def __init__(self):
        pass
    
    def create(self, newDetails: dict):
        """Updates the details of the user. 
        The new details are passed as a dictionary."""

        for key, value in newDetails.items():
            if key == "_id":
                self._userId = value
            elif key == "username":
                self._username = value
            elif key == "password":
                self._password = value
            elif key == "firstName":
                self._firstName = value
            elif key == "lastName":
                self._lastName = value
            elif key == "bankAccount":
                self._bankAccount = value
            else:
                raise Exception("Invalid key")

            self._balance = 0.0

    def update(self, newDetails: dict):
        """Updates the details of the user. 
        The new details are passed as a dictionary."""

        for key, value in newDetails.items():
            if key == "password":
                self.password = value
            elif key == "firstName":
                self.firstName = value
            elif key == "lastName":
                self.lastName = value
            elif key == "bankAccount":
                self.bankAccount = value
            else:
                raise Exception("Invalid key")

    @property
    def userId(self):
        return self._userId
    @userId.setter
    def userId(self):
        raise Exception("Cannot change user id")

    @property
    def username(self):
        return self._username
    @username.setter
    def username(self):
        raise Exception("Cannot change username")
    
    @property
    def password(self):
        return self._password
    @password.setter
    def password(self, newPassword: str):
        if self._password != newPassword:
            self._password = newPassword
        else:
            raise Exception("Password cannot be the same")

    @property
    def firstName(self):
        return self._firstName
    @firstName.setter
    def firstName(self, newFirstName: str):
        self._firstName = newFirstName
    
    @property
    def lastName(self):
        return self._lastName
    @lastName.setter
    def lastName(self, newLastName: str):
        self._lastName = newLastName
    
    @property
    def bankAccount(self):
        return self._bankAccount
    @bankAccount.setter
    def bankAccount(self, newBankAccount: str):
        self._bankAccount = newBankAccount
    
    @property
    def balance(self):
        return self._balance
    @balance.setter
    def balance(self, newBalance: float):
        self._balance = newBalance


    def viewDetails(self):
        return [
            ["username", self.username],
            ["First name", self.firstName],
            ["Last name", self.lastName],
            ["Bank account", self.bankAccount],
            ["Current balance", self.balance]
        ]
    
    def createRequestToUpdate(self):
        print("1. Password")
        print("2. First name")
        print("3. Last name")
        print("4. Bank account")
        print("5. Exit")
        option = int(input("Enter option: "))
        if option == 1:
            self.password = input("Enter new password: ")
        elif option == 2:
            self.firstName = input("Enter new first name: ")
        elif option == 3:
            self.lastName = input("Enter new last name: ")
        elif option == 4:
            self.bankAccount = input("Enter new bank account: ")
        elif option == 5:
            return
        else:
            print("Invalid option")
            return
        print("Details updated")
        return vars(self)
    
    def signUp(self):
        self.username = input("Enter username: ")
        self.password = input("Enter password: ")
        self.firstName = input("Enter first name: ")
        self.lastName = input("Enter last name: ")
        self.bankAccount = input("Enter bank account: ")
        return vars(self)

    def signIn(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        return {'username': username, 'password': password}

    def populateDetails(self, response: dict):
        self.initializer(
            userId=response["userId"],
            username=response["username"],
            password=response["password"],
            firstName=response["firstName"],
            lastName=response["lastName"],
            bankAccount=response["bankAccount"]
        )

