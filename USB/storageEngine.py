import os, hashlib    
from UserInterface import User

class ManageStorage:
    def __init__(self, path):
        self.pathstore = path+"/data/Storage.data"
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
        bpwdhash = []
        bpermissions = []
        broot = []
        buser = list(bytearray(USER.user.encode("utf-8")))
        bpwdhash = list(bytearray(USER.hasher))
        bpermissions = USER.perms%256
        broot = list(bytearray(USER.home.encode("utf-8")))
        print(broot)
        a = 20-buser.__len__()
        for i in range(0, a):
            buser.insert(0,0)

        a = 40-bpwdhash.__len__()
        for i in range(0, a):
            bpwdhash.insert(0,0)
        a = 39-broot.__len__()
        for i in range(0, a):
            broot.insert(0,0)
            
        Total = buser
        Total.extend(bpwdhash)
        Total.extend(broot)
        Total.append(bpermissions)
        if Total.__len__() == 100:
            self.content.extend(Total)
            self.update()
        else:
            print("Internal error: User not allowed to be registered")
    def getUser(self, user)-> User|None:
        i=0
        if self.content.__len__()<100:
            return None
        while i<self.content.__len__():
            buser = self.content[i:i+20]
            bpwdhash = self.content[i+20:i+60]
            broot = self.content[i+60:99]
            bperms = self.content[i+99]
            
            while True:
                if buser[0] == 0:
                    del buser[0]
                else:
                    break
            
            while True:
                if bpwdhash[0] == 0:
                    del bpwdhash[0]
                else:
                    break

            while True:
                if broot[0] == 0:
                    del broot[0]
                else:
                    break
            
            
            if (bytearray(buser)).decode("utf-8") == user:
                return User(bytearray(buser).decode("utf-8"), bytearray(bpwdhash), bytearray(broot).decode("utf-8"), bperms)
            i+=100
        return None
    
    def update(self):
        new = open(self.pathstore, "wb")
        new.write(bytearray(self.content))
        new.close()

