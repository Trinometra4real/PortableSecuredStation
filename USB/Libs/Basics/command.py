import os    

def pwd(data) :
    path = data[1][0]
    return [path, os.path.realpath(path)]

def ls(data)->list:
    liste = ""
    path = data[1][0]
    if data[0] != []:
        path=data[0][0]
    else:
        path="."
    
    for element in os.listdir(path):
        if os.path.isdir(path+"/"+element):
            liste = liste + "d - "+element + "\n"
        elif os.path.isfile(path+"/"+element):
            liste = liste + "f - "+element + "\n"
    return [liste, os.path.realpath(path)]

def cd(data):
    path = data[1][0]
    root = data[1][1]
    params = data[0]
    if (data[0]==[]):
        return ["", os.path.realpath(root)]
    if (os.path.exists(path+"/"+params[0])):
        path = str(os.path.realpath(path+"/"+params[0]))
        return ["changed current directory to "+path, path]
    else:
        return ["This directory do not exists", os.path.realpath(path)]
    
def createusb(data):
    path = data[1][0]
    root = data[1][1]
    params = data[0]
    if (os.path.exists(params[0])):
        os.system("unzip -r "+root+"/USB.zip -d "+params[0])
        return ["Successfuly setted up !", path]
    else:
        return ["Inexistant path, please retry with another one", path]

def updateusb(data):
    path = data[1][0]
    root = data[1][1]
    params = data[0]
    if (os.path.exists(params[0])):
        os.system("unzip -or "+root+"/USB.zip -d "+params[0])
        return ["Successfuly setted up !", path]
    else:
        return ["Inexistant path, please retry with another one", path]



command = {
    "pwd":pwd,
    "ls":ls,
    "cd":cd,
    "createusb": createusb,
    "updateusb": updateusb
}