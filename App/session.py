from getpass import getpass
import os, hashlib, time, rsa
import infos, command
from keyholder import KeyHolder, GenNewKeys
from storageEngine import ManageStorage, User
__all__ = ["Session", "User"]

"""
Couche 3:Session
"""

class Session:
    def __init__(self, path):
        self.primary = {
            "help": self.help,
            "exit": self.exit,
            "install": self.install,
            "update": self.update,
        }
        self.command = command.command.copy()
        self.helpCommand = infos.helpCommand.copy()
        self.Running = True
        self._login = False
        self.permission = 0
        self.path = ""
        self.root = path
        print(self.root)
        self.fileManager = ManageStorage(path)
        self.USER = None
        if os.path.exists(self.root+"/home"):
            if os.path.isdir(self.root+"/home"):
                pass
            else:
                os.mkdir(self.root+"/home")
        else:
            os.mkdir(self.root+"/home")
        print("root is :"+self.root)
        
        time.sleep(1.0)
        
    def login(self):
        while not self._login:
            user = input("Enter user (specials character excluded): ")
            passphrase = getpass("Enter password: ").encode("utf-8")
            hasher = hashlib.md5()
            hasher.update(passphrase)
            pwd = hasher.digest()
            USER = self.fileManager.getUser(user, pwd)
            print(user)
            print(list(bytearray(user.encode("utf-8"))))
            if Session.correct_User(user):
                if USER != None:
                    if USER.checkPass():
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
                    GenNewKeys(self.root+"/home/"+user, pwd)
                    print("Keyholder Generated")
                    new=open(self.root+"/home/"+user+"/DataUser.pack", "w")
                    new.write("")
                    new.close()
                    USER = User(user, pwd, self.root+"/home/"+user, 255)

                    if self.fileManager.storeUser(USER):
                        print("user added to DB")
                        self.USER=USER
                        self._login = True
                        self.path=self.USER.home
                        if not os.path.exists(self.path):
                            os.mkdir(self.path)              
                        
                        print("Logged into a new account, "+self.USER.user)
                        self.fileManager.update()
                    else:
                        print("Failed to add user to the Database")
            else:
                print("User format is incorrect, please retry:\nA user name must be smaller than 20 characters.")
                
        time.sleep(1.0)

    def correct_User(user):
        string  = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0987654321 _-()[]"
        for char in user:
            if not char in string:
                return False
        return True
    
    def help(self, params):
        out = ""
        for element in self.helpCommand.keys():
            out = out +element+" : " + self.helpCommand[element] + "\n"
        return out
    
    def start(self):
        while self.Running and self._login:
            command = input("@localhost~$>").split(" ")
            if command[0] in self.primary.keys():
                try:
                    print(self.primary[command[0]](command[1:]))
                except:
                    print("incorrect command, please use help command")

            elif command[0] in command.keys():
                try:
                    [output, self.path ] = self.command[command[0]]([command[1:], [self.path, self.root]])
                    print(output)
                except:
                    print("incorrect command")
                

            else:
                print("incorrect command, please use help command")

    def install(self, package):
        # take package folder and place it in Lib dir
        if os.path.exists(package):
            if os.path.isdir(package):
                os.system("mv "+package+" "+self.root+"/App/Libs/")
                print("Installation done, updating global app")
                self.update()
            else:
                return "Cancelled: Package is not a directory"
        else:
            return "Cancelled: Package location isn't correct"

    
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
        new.close()
        self.exit()


    def exit(self, params):
        self.Running = False
        return "Exiting session"
    
if __name__ == '__main__':
    main()