import os   
from UserInterface import User

class ManageStorage:
    def __init__(self, path):
        self.pathstore = path+"/data/Storage.data"
        if os.path.exists(path+"/data"):
            if os.path.isdir(path+"/data"):
                pass
            else:
                os.mkdir(path+"/data")
        else:
            os.mkdir(path+"/data")
            
                
        if os.path.exists(self.pathstore):
            new = open(self.pathstore, "rb")
            self.content = list(new.read())
            new.close()
            if self.content == [0]:
                self.content = []
            
        else:
            new = open(self.pathstore, "wb")
            self.content = []
            new.write(bytearray([0]))
            new.close()
            
        
    def storeUser(self, USER:User):
        buser = []
        
        bpermissions = []
        broot = []
        buser = list(bytearray(USER.user.encode("utf-8")))
        bpermissions = USER.perms%256
        broot = list(bytearray(USER.home.encode("utf-8")))
        a = 20-buser.__len__()
        for i in range(0, a):
            buser.insert(0,0)

        a = 139-broot.__len__()
        for i in range(0, a):
            broot.insert(0,0)
        print("buser ", buser.__len__())
        Total = buser
        Total.extend(broot)
        Total.append(bpermissions)
        
        if Total.__len__() == 160:
            self.content.extend(Total)
            self.update()
            return True
        else:
            print("Internal error: User not allowed to be registered")
            return False
        
        
    def getUser(self, user, pwd)-> User|None:
        i=0
        if self.content.__len__()<160:
            return None
        while i<self.content.__len__():
            buser = self.content[i:i+20]
            broot = self.content[i+20:159]
            bperms = self.content[i+159]
            
            while True:
                if buser[0] == 0:
                    del buser[0]
                else:
                    break
          

            while True:
                if broot[0] == 0:
                    del broot[0]
                else:
                    break
            
            
            if (bytearray(buser)).decode("utf-8") == user:
                return User(bytearray(buser).decode("utf-8"), pwd, bytearray(broot).decode("utf-8"), bperms)
            i+=100
        return None
    
    def update(self):
        new = open(self.pathstore, "wb")
        new.write(bytearray(self.content))
        new.close()

