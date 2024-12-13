import socket, rsa, json, os, threading
from datetime import datetime


class challenge:
    def __init__(self, message="", user="",sign="", public="", load=""):
        if load == "":
            self.message = message
            self.date = str(datetime.now())
            self.user = user
        else:
            datagramme = json.loads(load)
            self.message = datagramme.message
            self.date = datagramme.date
            self.user = datagramme.user

    def ToJson(self):
        data = {
            "message": self.message,
            "date": self.date,
            "user": self.user,
            "sign": self.sign,
            "pubkey": self.public
        }
        return json.dumps(data)

class Server:
    def __init__(self, ip:str, port:int, rootrsa:str):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))
        self.Running = True
        self.rootrsa = rootrsa
    


    def start(self):
        self.connections = []
        while self.Running:
            self.server.listen(4)
            rmt_socket, rmt_addr  = self.server.accept()
            newConn = Connection(rmt_socket, rmt_addr)
            newTask = threading.Thread(target=newConn.start)
            self.connections.append([newConn, newTask])
            self.connections[-1][1].start()
            print(f"{self.connections.__len__()} sockets used")
            for element in connections:
                if not element[0].is_alive():
                    del element
        for element in self.connections:
            element[0].kill()
        Actives = self.connections.__len__()
        for element in self.connections:
            if element[0].is_alive():
                Actives+=1

        
        print("Server successfuly shutdown")
        return True

    def stop(self):
        self.Running = False

class Connection:
    def __init__(self, remote_socket:socket.socket, remote_addr, rootrsa):
        self.socket = remote_socket
        self.rmtAddr = remote_addr
        self.running = True
        self.rootrsa = rootrsa
        self.logged = False

    def start(self):
        data = self.socket.recv(1024)
        datagram = data.decode("utf-8")
        try:
            Cha = challenge(load=datagram)
            message = Cha.message
            sign = Cha.sign
            user = Cha.user

        except:
            self.running = False

        if  os.path.exists(self.rootrsa+"/Server/Private") and os.path.exists(self.rootrsa+"/Server/Public"):
            new = open(self.rootrsa+"/Server/Private", "rb")
            private = rsa.PrivateKey.load_pkcs1(new.read()) 
            new.close()
            new = open(self.rootrsa+"/Server/Public", "rb")
            public = rsa.PublicKey.load_pkcs1(new.read()) 
            new.close()
            self.KeyHolder = Encryption(ExernKey, [public, private])
            
        else:
            self.KeyHolder = Encryption(ExernKey)
        if not self.KeyHolder.CheckKey(message, Sign):
            resp = "EROR: AUTH\nMISMATCH SIGN AND PUBLIC KEY\nCONN: CLOSED".encode("utf-8")
            resp = rsa.encrypt(resp, self.KeyHolder.externalPublic)
            signed = rsa.sign(resp, self.KeyHolder.keys[1], "SHA-512")
            response = challenge(resp, "root", signed, self.KeyHolder.public)
            self.socket.send(response.ToJson().encode("utf-8"))
            self.running = False
        else:
            if user in os.listdir("data/Users/"):
                new = open("data/Users/"+user+"/public","rb" )

                if rsa.PublicKey.load_pkcs1(new.read()) == self.ExernKey:
                    self.logged = True
                    self.StartCom()
                else:
                    self.Register()
            else:
                self.Register()

    def StartCom(self):
        if self.running:
            return

    def Register(self):
        if self.running:
            return

    def is_alive(self):
        return self.running
        
    def kill(self):
        self.socket.close()

class Encryption:

    def __init__(self, externalPublic, keys=[]):
        if keys==[]:
            self.generateKeys()
        else:
            self.public = keys[0]
            self.private = keys[1]
        self.externalPublic = externalPublic

    def generateKeys(self):
        self.keys = [None,None]
        self.public, self.private = rsa.newkeys(2048)

    def CheckKey(self, challenge:str, sign):
        return rsa.verify(challenge, sign, self.externalPublic)
        

    def Decrypt(self, challenge):
        decoded = rsa.decrypt(challenge.message, self.keys[1])
        return decoded
        
    def Crypt(self, challenge):
        encoded = rsa.encrypt(challenge.message, self.externalPublic)
        return encoded
