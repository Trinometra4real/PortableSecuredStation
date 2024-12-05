from infos import *
from getpass import getpass
import os, hashlib, time

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
        
    def login(self):
        while not self._login:
            user = input("Enter user: ").replace(" ", "").capitalize()
            pwd = getpass("Enter password: ").encode("utf-8")
            hasher = hashlib.md5()
            hasher.update(pwd)
            pwd = hasher.digest()
            USER = self.fileManager.getUser(user)
            print(USER)
            if USER != None:
                if USER.checkPass(pwd):
                    self.USER=USER
                    print("Logged as "+user)
                    self._login = True
                    self.path = self.root+self.USER.root
 
                else:
                    print("incorrect password")
                    
            else:
                USER = User(user, pwd, "/data/home/"+user+"/", 255)
                self.fileManager.storeUser(USER)
                self._login = True
                self.USER=USER
                print("Logged into a new account, "+self.USER.user)
                self.path=self.root+self.USER.root
                if not os.path.exists(self.path):
                    os.mkdir(self.path)
                
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
                print(self.command[command[0]](command[1:]))
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

if __name__ == '__main__':
    main()
    
