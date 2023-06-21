import User
import AppClientSide

if __name__ == "__main__":
    
    User = User.User()
    App = AppClientSide.AppClientSide(User)
    App.start()