import os, hashlib    
from UserInterface import User

class ManageStorage:
    def __init__(self, path):
        self.pathstore = path+"/data/Storage.data"
        print(self.pathstore)
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
        broot = list(bytearray(USER.root.encode("utf-8")))
        
        a = 20-buser.__len__()
        for i in range(0, a):
            buser.insert(0,0)

        a = 20-bpwdhash.__len__()
        for i in range(0, a):
            bpwdhash.insert(0,0)
        a = 59-broot.__len__()
        for i in range(0, a):
            broot.insert(0,0)
            
        Total = buser
        Total.extend(bpwdhash)
        Total.extend(broot)
        Total.append(bpermissions)
        print(Total.__len__())
        self.content.extend(Total)
        self.update()
    
    def getUser(self, user)-> User|None:
        i=0
        print(self.content.__len__())
        if self.content.__len__()<100:
            return None
        while i<self.content.__len__():
            print(i)
            buser = self.content[i:i+20]
            bpwdhash = self.content[i+20:i+40]
            broot = self.content[i+40:99]
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

class File:
    def __init__(self, path, content):
        self.path = path
        self.content = content
    
    def get(self):
        return self.content
    
    def set(self, content:list):
        self.content = content.copy()
        

    def write(self):
        try:
            new = open(self.path, "wb")
            new.write(bytearray(self.content))
            new.close()
            return True
        except FileNotFoundError:
            print("failed to write up the file")
            return False
        except:
            print("unknown error")
            return False
    def getPath(self):
        return self.path