import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.245.234', 2900))
client_socket.send("test connection".encode("utf-8"))

print("end")


