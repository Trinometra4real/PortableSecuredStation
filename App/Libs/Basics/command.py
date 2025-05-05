import os    


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
    
def createusb(self, params):
    if (os.path.exists(params[0])):
        os.system("unzip -r "+self.root+"/USB.zip -d "+params[0])
        return "Successfuly setted up !"
    else:
        return "Inexistant path, please retry with another one"

def updateusb(self, params):
    if (os.path.exists(params[0])):
        os.system("unzip -or "+self.root+"/USB.zip -d "+params[0])
        return "Successfuly setted up !"
    else:
        return "Inexistant path, please retry with another one"



command = {
    "exit": exit,
    "ls":ls,
    "cd":cd
}