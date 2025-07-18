from keyholder import KeyHolder, GenNewKeys
from getpass import getpass
import os, hashlib, time, rsa


from storageEngine import ManageStorage, User
__all__ = ["Session", "User"]

"""
Couche 3:Session
"""

class Session:
    def __init__(self, path):
        self.Running = True
        self._login = False
        self.permission = 0
        self.path = path
        self.root = path
        self.primary = {
            "help": self.help,
            "exit": self.exit,
            "install": self.install,
            "update": self.update,
            "dumpfiles": self.dumpFiles,
            "importall": self.importAll
        }
        self.helpPrimary = {
            "help": "usage:\n\thelp [CMD]\n\ndisplay some hints about the use of different commands",
            "exit": "usage:\n\texit\n\nClose this session and save the keys of the user",
            "install" : "usage:\n\tinstall [package_path]\n\npermit to install packages, and includes more commands",
            "update": "usage:\n\tupdate\n\nrefresh the application by listing packages, and reordening links/pointers",
            "dumpfiles": "usage:\n\tdumpfiles\n\nWrite all files stored in the user's home",
            "importall":"usage:\n\timportall\n\nImport all the files from the clearfiles folder, and then erase them"
        }
        
        try:
            import infos, commands
        except:
            print("Failed to import methods, updating local libs")
            ### update installed package list ###
            os.remove(self.root+"/infos.py")
            os.remove(self.root+"/commands.py")
            packlist = []
            
            for pack in os.listdir(self.root+"/Libs"):
                
                package = self.root+"/Libs/"+pack
                if os.path.isdir(package):
                    packlist.append(pack)
            #### command pointers update ####
            new = open(self.root+"/commands.py", "a")
            new.write("#### IMPORT ####")
            for pack in packlist:
                new.write("\nfrom Libs import "+pack)
            new.write("\n\n#### INIT ####\ncommand={}\n\n####  BUILDUP ####")
            for pack in packlist:
                new.write("\ncommand.update("+pack+".command.command)")
            new.close()

            ### help command update ###
            new = open(self.root+"/infos.py", "a")
            new.write("#### IMPORTS ####\n")
            for pack in packlist:
                new.write("from Libs import "+pack+"\n")

            new.write("\n#### INIT ####\nhelpCommand = {}\n\n#### BUILDUP ####\n")
            for pack in packlist:
                new.write("helpCommand.update("+pack+".infos.helpCommand)\n")
            new.close()
            import infos, commands
        self.command = commands.command.copy()
        args = self.command.keys()
        self.userInit = []
        self.killSign = []
        toDelete = []
        
        for element in self.command.keys():
            if (element.startswith("INIT")):
                self.userInit.append(self.command[element])
                toDelete.append(element)
            elif (element.startswith("CLOSE")):
                self.killSign.append(self.command[element])
                toDelete.append(element)

        for element in toDelete:
            del self.command[element]

        self.helpCommand = infos.helpCommand.copy()
        self.helpCommand.update(self.helpPrimary)
        self.fileManager = ManageStorage(self.root)
        print(path)
        self.USER = None
        if os.path.exists(self.root+"/home"):
            if os.path.isdir(self.root+"/home"):
                pass
            else:
                os.mkdir(self.root+"/home")
        else:
            os.mkdir(self.root+"/home")
       
        
    def login(self):
        while not self._login:
            user = input("Enter user (specials character excluded): ")
            passphrase = getpass("Enter password: ").encode("utf-8")
            hasher = hashlib.sha256()
            hasher.update(passphrase)
            pwd = hasher.digest()
            USER = self.fileManager.getUser(user, pwd)

            if Session.correct_User(user):
                if USER != None:
                    if USER.checkPass():
                        self.USER=USER
                        print("Logged as "+user)
                        self._login = True
                        self.path = self.USER.home
    
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
                            os.system("rm -r "+self.root+"/home/"+user+"/*")
                        except:
                            pass
                        try:
                            os.rmdir(self.root+"/home/"+user)
                        except:
                            pass
                    os.mkdir(self.root+"/home/"+user)
                    os.mkdir(self.root+"/home/"+user+"/clearfiles")
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

    def start(self):
        self.login()
        if self._login:
            for element in self.userInit:
                element(self.USER)
        else:
            print("No user logged, exiting")
            self._login = False
            
        while self.Running and self._login:
            cmd = input(self.USER.user+"@localhost~$>").split(" ")
            if cmd!=['']:
                if cmd[0] in self.primary.keys():
                    try:
                        print(self.primary[cmd[0]](cmd[1:]))
                    except:
                        print("incorrect command, please use help command")    
                        

                elif cmd[0] in self.command.keys():
                    
                    args = cmd[1:].copy()
                    args.extend([self.path, self.root])
                    try:
                        [output, self.path] = self.command[cmd[0]]( args )
                        print(output)
                    except:
                        print("incorrect command, please use help command")
            
    def help(self, params):
        out = ""
        if params!=[]:
            if params[0] in self.helpCommand.keys():
                out+=self.helpCommand[params[0]]
        else:
            for key in self.helpCommand.keys():
                out+=self.helpCommand[key]+"\n______________________________\n"
        return out
    
    def exit(self, params=None):
        self.fileManager.update()
        self.USER.closeFiles()
        for element in self.killSign:
            element()
            
        self.Running = False
        return "Exiting session"
    
    def install(self, data:list):
        package = data[0]
        print(package)
        
        # take package folder and place it in Lib dir
        if (package.startswith(".")):
            package = package.replace(".", self.path)
        elif (not package.startswith("/")):
            package = self.path+package
        print(package)
        if os.path.exists(package):
            if os.path.isdir(package):
                if ("infos.py" in os.listdir(package) and "command.py"in os.listdir(package) and "__init__.py" in os.listdir(package) and "required.sh" in os.listdir(package)):
                    os.system("mv "+package+" "+self.root+"/Libs/")
                    print("installing required modules")
                    os.system("chmod +x "+self.root+"/Libs/"+package.split("/")[-1]+"/required.sh;\n/bin/bash "+self.root+"/Libs/"+package.split("/")[-1]+"/required.sh")
                    print("Installation done, updating global app")
                    return self.update()
                else:
                    return "Package is not an installable directory"
            else:
                return "Cancelled: Package is not a directory"
        else:
            return "Cancelled: Package location isn't correct"
        
    def dumpFiles(self, params=None):
        self.USER.dumpAll()
        return "Dumped files"
    
    def importAll(self, params=None):
        self.USER.importAll()
        return "Imported Files"
    
    def correct_User(user):
        string  = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0987654321 _-()[]"
        for char in user:
            if not char in string:
                return False
        return True
    
    def update(self, params=None):
        ### update installed package list ###
        os.remove(self.root+"/infos.py")
        os.remove(self.root+"/commands.py")
        packlist = []
        
        for pack in os.listdir(self.root+"/Libs"):
            
            package = self.root+"/Libs/"+pack
            if os.path.isdir(package):
                packlist.append(pack)
        #### command pointers update ####
        new = open(self.root+"/commands.py", "a")
        new.write("#### IMPORT ####")
        for pack in packlist:
            new.write("\nfrom Libs import "+pack)
        new.write("\n\n#### INIT ####\ncommand={}\n\n####  BUILDUP ####")
        for pack in packlist:
            new.write("\ncommand.update("+pack+".command.command)")
        new.close()

        ### help command update ###
        new = open(self.root+"/infos.py", "a")
        new.write("#### IMPORTS ####\n")
        for pack in packlist:
            new.write("from Libs import "+pack+"\n")

        new.write("\n#### INIT ####\nhelpCommand = {}\n\n#### BUILDUP ####\n")
        for pack in packlist:
            new.write("helpCommand.update("+pack+".infos.helpCommand)\n")
        new.close()
        return self.exit()


if __name__ == '__main__':
    main()
    
