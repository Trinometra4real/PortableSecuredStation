from getpass import getpass
import os, time
from infos import *

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
        if os.path.exists(self.root+"/home"):
            if os.path.isdir(self.root+"/home"):
                pass
            else:
                os.mkdir(self.root+"/home")
        else:
            os.mkdir(self.root+"/home")
        print("root is :"+self.root)
        
        time.sleep(1.0)

    def start(self):
            
        while self.Running and self._login:
            command = input("@localhost~$>").split(" ")
            
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
    
    def install(self, params):
        os.system("unzip -r "+params+" -d "+self.root+"/bin/")
        
    def createusb(self, params):
        if (os.path.exists(params[0])):
            os.system("unzip -r "+self.root+"/USB.zip -d "+params[0])
            return "Successfuly setted up !"
        else:
            return "Inexistant path, please retry with another one"
        
    def update(self, params):
        os.system("/bin/bash "+self.root+"/installer.sh")
        
    def updateusb(self, params):
        if (os.path.exists(params[0])):
            os.system("unzip -or "+self.root+"/USB.zip -d "+params[0])
            return "Successfuly setted up !"
        else:
            return "Inexistant path, please retry with another one"

if __name__ == '__main__':
    main()