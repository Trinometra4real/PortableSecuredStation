import os   
from UserInterface import User

class ManageStorage:
    def __init__(self, root):
        self.root=root
        self.path = root+"/data/Storage.data"
        if os.path.exists(root+"/data"):
            if os.path.isdir(root+"/data"):
                pass
            else:
                os.mkdir(root+"/data")
        else:
            os.mkdir(root+"/data")
            
                
        if os.path.exists(self.path):
            new = open(self.path, "rb")
            self.content = list(new.read())
            new.close()
            if self.content == [0]:
                self.content = []
            
        else:
            new = open(self.path, "wb")
            self.content = []
            new.write(bytearray([0]))
            new.close()
            
        
    def storeUser(self, USER:User):
        buser = []
        
        bpermissions = []
        broot = []
        buser = list(bytearray(USER.user.encode("utf-8")))
        bpermissions = USER.perms%256
        broot = list(bytearray(USER.home.replace(self.root, "").encode("utf-8")))
        print("path without root: "+USER.home.replace(self.root, ""))
        a = 20-buser.__len__()
        for i in range(0, a):
            buser.insert(0,0)

        a = 139-broot.__len__()
        for i in range(0, a):
            broot.insert(0,0)
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
        while i+160<=self.content.__len__():
            buser = self.content[i:i+20]
            broot = self.content[i+20:i+159]
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
                return User(bytearray(buser).decode("utf-8"), pwd, self.root+bytearray(broot).decode("utf-8"), bperms)
            i+=160
        return None
    
    def update(self):
        new = open(self.path, "wb")
        new.write(bytearray(self.content))
        new.close()

