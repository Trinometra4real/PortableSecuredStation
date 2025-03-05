import socket
import threading
class peer2peer(ip, user:User):
    # 9000: broadcast
    # 9001: liaison
    #
    def __init__(self, ip):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("", 9000))
        sock.listen(5)
        while Running:
            recv, remaddr = sock.accept()
            t = threading.Thread(target=self.handleConn(recv, remaddr))
            t.start()

    def handleConn(self, sock:socket.socket, remaddr:str):

        


