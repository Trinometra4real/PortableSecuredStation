NAME = [0, 255,245,235, 0]
SCONTENT = [0, 255,222,233, 0]
EPACK = [255,200,10,200,255]
import os
from keyholder import KeyHolder
### PATTER:  [NAME]...[SCONTENT]...[EPACK]/[NAME]...

class File:
    def __init__(self, path:str, content:bytes):
        self.path = path
        self.content = content
        print("added file: "+self.getPath())
        
    def write(self):
        new = open(self.path, "wb")
        new.write(self.content)
        new.close()
            
    def getContent(self):
        return self.content
        
    def getPath(self):
        return self.path
    
    
class User:
    def __init__(self, user:str, pwd:bytes,home:str, perms:int):
        self.user = user
        self.perms = perms
        self.home = home
        self.hasher = pwd
        self.Files = []
        if os.path.exists(self.home+"/private.key") and os.path.exists(self.home+"/public.crt"):
            self.keyholder = KeyHolder(self.home, self.hasher)
            if (self.keyholder.purifyKey(self.hasher)):
                print("Keyholder initialized")
            else:
                print("Incorrect password, exiting")
                exit(0)
            
        else:
            print("Fatal Error: no cipher keys found")
            exit(0)
    
        try:
            new = open(home+"/DataUser.pack", "rb")
            encryptedData = new.read()
            new.close()
            if list(bytearray(encryptedData))!=[]:
                self.row = self.keyholder.decrypt(encryptedData)
            else:
                self.row=[]
        except FileNotFoundError:
            print("User data reset !")
            new = open(home+"/DataUser.pack", "wb")
            new.write(bytearray([0]))
            new.close()
            
        self.loadData()

    def loadData(self):
        self.row=list(bytearray(self.row))
        
        if (self.row==EPACK):
            print("No files found for user")
            return
        i=0
        content = []
        name = []
        mode = 1
        while True:

            if (self.row.__len__()<=i):
                print("End of file, no data detected")
                break
            else:
                if (self.row[i:i+5]==NAME):
                    if content!=[]:
                        self.Files.append(File(self.home+bytes(bytearray(name)).decode("utf-8"), bytes(bytearray(content))))
                    mode = (mode+1)%2
                    name = []
                    content = []
                    i+=5
                    
                elif (self.row[i:i+5]==SCONTENT):
                    mode = (mode+1)%2
                    i+=5
                elif (self.row[i:i+5]==EPACK):
                    if content!=[]:
                        self.Files.append(File(self.home+bytes(bytearray(name)).decode("utf-8"), bytes(bytearray(content))))
                    break
                    
                elif mode == 0:
                    name.append(self.row[i])
                    i+=1
                    
                elif mode==1:
                    content.append(self.row[i])
                    i+=1
        self.dumpAll()
                    
    def checkPass(self):
        return self.keyholder.purifyKey(self.hasher)
    
    def dumpAll(self):
        for files in self.Files:
            print(files.getPath())
            files.write()
            
        self.Files = []

    def closeFiles(self):
        self.importAll()
        FileContent = []
        for element in self.Files:
            FileContent.extend(NAME)
            print(element.getPath())
            FileContent.extend(list(bytearray(element.getPath().replace(self.home, "").encode("utf-8"))))
            FileContent.extend(SCONTENT)
            FileContent.extend(list(bytearray(element.getContent())))
        FileContent.extend(EPACK)
        FileContent=bytes(bytearray(FileContent))
        new = open(self.home+"/DataUser.pack", "wb")
        new.write(self.encrypt(FileContent))
        new.close()

    def importAll(self):
        for file in os.listdir(self.home+"/clearfiles"):
            if (os.path.isfile(self.home+"/clearfiles/"+file)):
                new = open(self.home+"/clearfiles/"+file, "rb")
                content = new.read()
                new.close()
                self.Files.append(File(self.home+"/clearfiles/"+file, content))
                os.remove(self.home+"/clearfiles/"+file)
                
    def encrypt(self, msg:bytes) -> bytes:
       
        return self.keyholder.encrypt(msg)
    
    def decrypt(self, msg:bytes) -> bytes:
        return self.keyholder.decrypt(msg)
    
            
        
