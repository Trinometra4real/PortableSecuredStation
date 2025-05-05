import socket
import threading
from message import Message
from UserInterface import User
import time 
import rsa
class peer2peer:
    # 9000: broadcast
    # 9001: liaison
    #
    def __init__(self, ip, user:User):
        self.Listening = True
        self.user = user
        t=threading.Thread(target=self.search, args=())
        t.start()
        self.MSG = Message(user)

    def search(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        while self.Listening:
            recv, remaddr = sock.accept()
            t = threading.Thread(target=self.handleConn(recv, remaddr))
            t.start()

    def connect(self, ip):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            sock.connect((ip, 9001))
            data = b"PUBLIC\n"+self.user.keyholder.public.save_pkcs1()


            self.MSG.loadData(data)
            sock.send(self.MSG.getTrame())
            if self.MSG.read(sock.recv(100)):
                dataresp = self.MSG.getResponse().split("\n")
                public = dataresp[1].encode()
                publicdist = rsa.PublicKey.load_pkcs1(public)
                data="SHARE FILE"
                self.MSG.loadData(data, publicdist, True)
                sock.send()
            else:
                sock.send("CLOSE CONN:403")
                print("Impossible to verify behavior")
                sock.close()
        except socket.herror:
            print("Connection failed")

        

    def broadCast(self):
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = "ASK CONNECTION"
        msg = Message(self.user.user, data)
        trame = msg.getTrame()
        while self.Listening:
            sock.sendto(trame, ("255.255.255.255", 9000))
            time.sleep(2)
    

    def handleConn(self, sock:socket.socket, remaddr:str):
        if self.MSG.read(sock.recv(100)):
            public = self.MSG.getResponse().split("\n")[1].encode()
            publicdist = rsa.PublicKey.load_pkcs1(public)
            self.MSG.loadData(self.user.keyholder.public.save_pkcs1(), publicdist, encoded=True)
            sock.send(self.MSG.getTrame())
        else:
            print("connection refused: Malformed transmission")
        

        


