from keyholder import KeyHolder, GenNewKeys
from infos import *
from getpass import getpass
import os, hashlib, time, rsa


from storageEngine import ManageStorage, User
__all__ = ["Session", "User"]

"""
Couche 3:Session
"""

class Session:
    def __init__(self, path):
        self.command = {
            "help": self.help,
            "exit": self.exit,
            "ls":self.ls,
            "cd":self.cd
        }
        self.Running = True
        self._login = False
        self.permission = 0
        self.path = ""
        self.root = path
        print(self.root)
        self.fileManager = ManageStorage(path)
        self.USER = None
        print("root is :"+self.root)
    def login(self):
        while not self._login:
            user = input("Enter user (specials character excluded): ")
            passphrase = getpass("Enter password: ").encode("utf-8")
            hasher = hashlib.md5()
            hasher.update(passphrase)
            pwd = hasher.digest()
            USER = self.fileManager.getUser(user)
            if Session.correct_User(user):
                if USER != None:
                    if USER.checkPass(pwd):
                        self.USER=USER
                        print("Logged as "+user)
                        self._login = True
                        self.path = self.root+self.USER.home
    
                    else:
                        print("incorrect password")
                        
                else:
                    if os.path.exists(self.root+"/home/"+user):
                        try:
                            os.remove(self.root+"/home/"+user+"/DataUser.pack")
                        except:
                            pass
                        try:
                            os.remove(self.root+"/home/"+user+"/private.key")
                        except:
                            pass
                        try:
                            os.remove(self.root+"/home/"+user+"/public.crt")
                        except:
                            pass
                        try:
                            os.rmdir(self.root+"/home/"+user)
                        except:
                            pass
                    os.mkdir(self.root+"/home/"+user)
                    print("Génération du porte-clés ...")
                    GenNewKeys(self.root+"/home/"+user, passphrase)
                    print("Keyholder Generated")
                    new=open(self.root+"/home/"+user+"/DataUser.pack", "w")
                    new.write("")
                    new.close()
                    USER = User(user, pwd, self.root+"/home/"+user, 255)

                    self.fileManager.storeUser(USER)
                    print("user added to DB")
                    self.USER=USER
                    self._login = True
                    self.path=self.USER.home
                    if not os.path.exists(self.path):
                        os.mkdir(self.path)              
                    
                    print("Logged into a new account, "+self.USER.user)
            else:
                print("User format is incorrect, please retry:\nA user name must be smaller than 20 characters.")
                
        time.sleep(1.0)

    def start(self):
        self.login()
        if self._login:
            pass
        else:
            print("No user logged, exiting")
            self._login = False
            
        while self.Running and self._login:
            command = input(self.USER.user+"@localhost~$>").split(" ")
            
            try:
                if command != " ":
                    print(self.command[command[0]](command[1:]))
                else:
                    pass
            except Exception as f:
                print(f)
                print("incorrect command, please use help command")
            
    def help(self, params):
        out = ""
        for element in helpCommand.keys():
            out = out +element+" : " + helpCommand[element] + "\n"
        return out
    
    def ls(self, params)->list:
        liste = ""
        print(self.path)
        for element in os.listdir(self.path):
            if os.path.isdir(self.path+element):
                liste = liste + "d - "+element + "\n"
            elif os.path.isfile(self.path+element):
                liste = liste + "f - "+element + "\n"
        return liste

    def cd(self, params):
        self.path = str(os.path.realpath(self.path+params[0]))+"/"
        return "changed current directory to "+self.path
    
    def exit(self, params):
        self.Running = False
        return "Exiting session"
    
    def correct_User(user):
        string  = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0987654321 _-()[]"
        for char in user:
            if not char in string:
                return False
        return True

if __name__ == '__main__':
    main()
    
