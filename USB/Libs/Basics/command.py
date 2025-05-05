import os    


def ls(data)->list:
    liste = ""
    path = data[1][0]
    print(path)
    for element in os.listdir(path):
        if os.path.isdir(path+element):
            liste = liste + "d - "+element + "\n"
        elif os.path.isfile(element):
            liste = liste + "f - "+element + "\n"
    return [liste, path]

def cd(data):
    path = data[1][0]
    root = data[1[1]]
    params = data[0]
    path = str(os.path.realpath(path+params[0]))+"/"
    return ["changed current directory to "+path, path]
    
def createusb(data):
    path = data[1][0]
    root = data[1[1]]
    params = data[0]
    if (os.path.exists(params[0])):
        os.system("unzip -r "+root+"/USB.zip -d "+params[0])
        return ["Successfuly setted up !", path]
    else:
        return ["Inexistant path, please retry with another one", path]

def updateusb(data):
    path = data[1][0]
    root = data[1[1]]
    params = data[0]
    if (os.path.exists(params[0])):
        os.system("unzip -or "+root+"/USB.zip -d "+params[0])
        return ["Successfuly setted up !", path]
    else:
        return ["Inexistant path, please retry with another one", path]



command = {
    "ls":ls,
    "cd":cd,
    "createusb": createusb,
    "updateusb": updateusb
}