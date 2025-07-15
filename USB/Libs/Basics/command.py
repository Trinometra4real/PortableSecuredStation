import os    

def pwd(data) :
    path = data[-2]
    return [os.path.realpath(path), os.path.realpath(path)]

def ls(data)->list:
    liste = ""
    path = data[-2]
    print(data)
    print(path)
    
    if (data[-2]!=data[0]):
        for element in os.listdir(path+"/"+data[0]+"/"):
            subject = os.path.realpath(path+"/"+data[0]+"/"+element)
            subjectname=subject.split("/")[-1]
            if os.path.isdir(subject):
                liste = liste + "d - "+subjectname + "\n"
            elif os.path.isfile(subject):
                liste = liste + "f - "+subjectname + "\n"
        return [liste, os.path.realpath(path+"/"+data[0])]    
    else:
        for element in os.listdir(path):
            if os.path.isdir(path+"/"+element):
                liste = liste + "d - "+element + "\n"
            elif os.path.isfile(path+"/"+element):
                liste = liste + "f - "+element + "\n"
        return [liste, os.path.realpath(path)]

def cd(data):
    print(data)
    path = data[-2]
    root = data[-1]
    newpath = data[0]
    
    if (data[0]==[] or data[0]==""):
        return [os.path.realpath(root), os.path.realpath(root)]
    else:
        print("Not absolute: "+path+"/"+newpath+"/")
        if (data[0].startswith("/")):
            print(data[0])
            if (os.path.exists(data[0])):
                path=data[0]
                return ["changed current directory to "+path, path]
            else:
                return ["Directory do not exist", path]
        elif (os.path.exists(path+"/"+newpath+"/")):
            
            path = str(os.path.realpath(path+"/"+newpath+"/"))
            print(path+"/"+newpath+"/")
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