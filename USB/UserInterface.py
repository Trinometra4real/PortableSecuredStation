SPATH = [0, 255,245,235, 0]
SCONTENT = [0, 255,222,233, 0]


class User:
    def __init__(self, user:str, pwd:bytes,home:str, perms:int):
        self.user = user
        self.perms = perms
        self.home = home
        self.hasher = pwd
        self.Data = []
        #new = open(home+"/DataUser.pack", "rb")
        #self.row = list(bytearray(new.read()))
        #new.close()

        #self.loadData()

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
                


        self.Data = fullbuffer.copy()
        del fullbuffer

    def checkPass(self,password:bytes):
        return self.hasher == password
                    

class UserStorage:
    def __init__(self, datapack:str):
        new = open(datapack, "rb")
        self.content = list(bytearray(new.read()))
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