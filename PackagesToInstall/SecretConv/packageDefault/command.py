class ClientSecretMsg: # Need to be initialise at the very beginning
    def __init__(self):
        self.port = 8080
        self.ip = "0.0.0.0"
        self.user= None

    def setServIp(self, ip:str):
        self.ip = ip.split(":")[0]
        self.port = ip.split(":")[1]

def InitUser(classObject:ClientSecretMsg, User):
    classObject.user= User

def setServIp(classObject:ClientSecretMsg, params):
    classObject.setServIp(params[0][0])

command = {
    "__init__" : ClientSecretMsg(),
    "__user__" : InitUser,
    "setservip": setServIp
}