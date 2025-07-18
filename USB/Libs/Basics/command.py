import os    

def pwd(data) :
    path = data[-2]
    return [os.path.realpath(path), os.path.realpath(path)]

def ls(data)->list:
    liste = ""
    path = data[-2]    
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
    path = data[-2]
    root = data[-1]
    newpath = data[0]
    
    if (data[0]==[] or data[0]==""):
        return ["Changed current directory to "+os.path.realpath(root), os.path.realpath(root)]
    else:
        if (data[0].startswith("/")):
            if (os.path.exists(data[0])):
                path=data[0]
                return ["Changed current directory to "+path, path]
            else:
                return ["Directory do not exist", path]
        elif (os.path.exists(path+"/"+newpath+"/")):
            
            path = str(os.path.realpath(path+"/"+newpath+"/"))
            return ["changed current directory to "+path, path]
        else:
            return ["This directory do not exists", os.path.realpath(path)]
    
def createusb(data):
    path = data[-2]
    root = data[-1]
    params = data[0]
    if (os.path.exists(params[0])):
        os.system("cp -r /var/lib/PSS/Libs/* "+params[0])
        return ["Successfuly setted up !", path]
    else:
        return ["Inexistant path, please retry with another one", path]

def updateusb(data):
    path = data[-2]
    root = data[-1]
    params = data[0]
    if (os.path.exists(params[0])):
        os.system("rm -f "+params[0]+"/Libs/*")
        os.system("cp /usr/lib/PSS/Libs/* "+params[0]+"/Libs/")
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