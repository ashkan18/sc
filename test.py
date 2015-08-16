import socket

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.connect(('0.0.0.0', 9090))
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(('0.0.0.0', 9099))
client_sock.sendall('123\n')

client_sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock2.connect(('0.0.0.0', 9099))
client_sock2.sendall('321\n')

server_sock.sendall('1|F|321|123\r\n')





