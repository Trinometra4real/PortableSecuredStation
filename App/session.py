from getpass import getpass
import os, time
import infos
from Libs.AppList import *
import commands
__all__ = ["Session", "User"]

"""
Couche 3:Session
"""

class Session:
    def __init__(self, path):
        self.primary = {
            "help": self.help,
            "exit": self.exit,
            "ls":self.ls,
            "cd":self.cd
        }
        self.command = commands.command.copy()
        self.helpCommand = infos.helpCommand.copy()
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

    def help(self, params):
        out = ""
        for element in helpCommand.keys():
            out = out +element+" : " + helpCommand[element] + "\n"
        return out
    
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

    def install(self, package):
        # take package folder and place it in Lib dir
        os.system("mv "+package+" "+self.root+"/App/Libs/")
        new = open(self.root+"/App/Libs/AppList.py", "a")
        new.write("from "+package+" import *\n")
        new.close()
    
    def update(self):
        ### update installed package list ###
        os.remove(self.root+"/App/infos.py")
        os.remove(self.root+"/App/commands.py")
        packlist = []
        
        for pack in os.listdir(self.root+"/App/Libs"):
            package = self.root+"/App/Libs/"+pack
            if os.path.isdir(package):
                packlist.append(pack)

        #### command pointers update ####
        new = open(self.root+"/App/commands.py", "a")
        new.write("#### IMPORT ####")
        for pack in packlist:
            new.write("from Libs import "+pack)
        new.write("\n#### INIT ####\ncommand={}\n\n####  BUILDUP ####")
        for pack in packlist:
            new.write("command.update("+pack+".Command)")
        new.close()

        ### help command update ###
        new = open(self.root+"/App/infos.py", "a")
        new.write("#### IMPORTS ####")
        for pack in packlist:
            new.write("from Libs import "+pack)

        new.write("\n#### INIT ####\nhelpCommand = {}\n\n#### BUILDUP ####")
        for pack in packlist:
            new.write("helpCommand.update("+pack+".helpCommand)")
        


    def exit(self, params):
        self.Running = False
        return "Exiting session"
    
if __name__ == '__main__':
    main()