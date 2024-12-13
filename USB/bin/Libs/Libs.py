import os, base64, rsa, time
from datetime import *
LOG = "/var/log/"
def checkStop(newServ):
    
    new = open("var/config.json", "r")
    config = json.loads(new.read())
    new.close()

    rootrsa = config["secserv"]["root"]
    port = config["secserv"]["port"]
    ip = config["net"]["ip"].split(".")
    ipBin = []
    for i in range(0, ip.__len__()):
        ipBin.append(int(ip[i]))
    empreinte = ip
    empreinte.extend(Libs.bin2octets(Libs.int2bin(port)))
    empreinte.append(0)
    empreinteOn = empreinte.copy()
    empreinteOff=empreinte.copy()
    empreinteOn[-1] = 1
    empreinteOff[-1] = 0
    while True:
        time.sleep(60.0)
        new = open("var/Appbin", "rb")
        secbin = list(new.read())
        if Libs.checkbin(secbin, empreinteOff):
            Log(SIGNATURE, "Stopping the server")
            newServ.Running = False
            break
        elif not Libs.checkbin(secbin, empreinteOn):
            Log(SIGNATURE, "Binary flag is corrupted !")
            newServ.Running = False
            break
        else:
            pass

def Log(signature:str, message:str):
    Date = str(datetime.now().date())
    Time = str(datetime.now().time())
    path = LOG+signature+Date+".log"
    new = open(path, "a")
    new.write("["+Date+"]"+" - "+message)
    new.close()
    

def checkAppBin(key:list, array:list):
    i=0
    while (i+key.__len__())<=(array.__len__()):
        if array[i:i+key.__len__()-1]:
            return True
        else:
            i+=1
    return False
        
class SecuredDataEncryption:
    def __init__(self,  root,public_key):
        self.root = root
        self.public_key = public_key
        
        if os.path.exists(root+"/PrivateMain.pem") and os.path.exists(root+"/PublicMain.pem"):
            self.keys = [None, None]
            new = open(root+"/PrivateMain.pem", "rb")
            self.keys[1] = rsa.PrivateKey._load_pkcs1_pem(new.read())
            new.close()
            new = open(root+"/PrivateMain.pem", "rb")
            self.keys[0] = rsa.PrivateKey._load_pkcs1_pem(new.read())
            new.close()
        else:
            self.genKey(root)
        
            
    
    def genKey(self):
        self.keys = [None, None]
        self.keys[0], self.keys[1] = rsa.newkeys(nbits=2048)
        new = open(self.root+"/PrivateMain.pem", "wb")
        new.write(self.keys[0].save_pkcs1())
        new.close()
        new=open(self.root+"/PublicMain.pem", "wb")
        new.write(self.keys[1].save_pkcs1())
        new.close()
        return
    
    def decryptData(self, data):
        decrypted = rsa.decrypt(data, self.keys[1])
        return decrypted
    
    def encryptData(self, data):
        encrypted = rsa.encrypt(data, self.keys[0])
        return encrypted
        
class Binary:
    def int2bin(value:int):
        x = 0
        out = []
        while 2**(x) <= value:
            x+=1
        
        while x >=0:
            if value >= 2**x:
                value = value%(2**x)
                out.append(1)
                x-=1
            else:
                out.append(0)
                x-=1

        return out

    def bin2octets(value:list):
        binary = []
        if value.__len__()%8 != 0:

            val = value.__len__()
            binlen = binary.__len__()

            while (val+binlen)%8!=0:
                binary.append(0)
                binlen = binary.__len__()

        binary.extend(value)
        octets = binary.__len__()//8-1
        out = []
        for i in range(0, octets+1):
            out.append(Binary.bin2int(binary[i*8:i*8+8]))
        return out




    def bin2int(value:list):
        out = 0
        for i in range(0, value.__len__()):
            if value[value.__len__()-1-i] == 1:
               out += 2**i 
            
        return out

