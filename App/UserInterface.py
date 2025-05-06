SPATH = [0, 255,245,235, 0]
SCONTENT = [0, 255,222,233, 0]
EPACK = [255,200,10,200,255]
import os
from keyholder import KeyHolder

class User:
    def __init__(self, user:str, pwd:bytes,home:str, perms:int):
        self.user = user
        self.perms = perms
        self.home = home
        print(home)
        self.hasher = pwd
        self.Data = []
        if os.path.exists(self.home+"/private.key") and os.path.exists(self.home+"/public.crt"):
            self.keyholder = KeyHolder(self.home, self.hasher)
            print("Keyholder initialized")
        else:
            print("Fatal Error: no cipher keys found")
            exit(0)
    
        try:
            new = open(home+"/DataUser.pack", "rb")
            encryptedData = list(bytearray(new.read()))
            new.close()
            if encryptedData!=[]:
                self.row = self.keyholder.decrypt(encryptedData)
            else:
                self.row=[]
        except FileNotFoundError:
            new = open(home+"/DataUser.pack", "wb")
            new.write(bytearray([0]))
            new.close()

        

        self.loadData()

    def loadData(self):
        i=0
        self.fullTree = []
        while i<self.row.__len__():
            methint = 0
            method = {0:[], 1:[]}  # 0:path | 1:content
            balise = {0:SCONTENT,1:SPATH}
            if self.row[i:i+5] != balise[methint]:
                method[methint].append(self.row[i])
                i+=1
            else:
                if methint == 1:
                    file = File(method[0], method[1])
                    self.fullTree.append(file)
                methint = (1+methint)%2
        self.Data = self.fullTree.copy()
        del self.fullTree

    def checkPass(self):
        return self.keyholder.purifyKey(self.hasher)

    def writeData(self):
        FileContent = []
        for element in self.fullTree:
            FileContent.extend(SPATH)
            FileContent.extend(element.getPath()) # getPath -> list[int]
            FileContent.extend(SCONTENT)
            FileContent.extend(element.get())
        FileContent.extend(EPACK)
        new = open(self.home+"/DataUser.pack", "wb")
        new.write(self.encrypt(bytes(bytearray(FileContent))))

    def encrypt(self, msg:bytes) -> bytes:
        return self.keyholder.encrypt(msg)

    def decrypt(self, msg:bytes) -> bytes:
        return self.keyholder.decrypt(msg)
    
            
        
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