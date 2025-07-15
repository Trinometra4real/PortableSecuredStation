from . import UserInterface
class TestUser:
    def __init__(self):
        print("user inited")
        pass
    
    def init(self, User:UserInterface.User):
        self.user = User
    
    def getUserName(self, params:list):
        
        return self.user.user
    def __close__(self):
        self.user=None
        
CLASS = TestUser()

    
command = {
    "INIT_test":CLASS.init,
    "getname": CLASS.getUserName,
    "test_close": CLASS.__close__
}