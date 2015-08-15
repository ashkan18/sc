import socket
from client_socket import ClientSocketThread
from service_socket import EventServiceSocketThread


class App(object):
    def __init__(self, ip, port, service_ip, service_port):
        self.threads = []
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.bind((ip, port))

        server_thread = EventServiceSocketThread(service_ip, service_port)
        server_thread.start()

    def run(self):
        while True:
            self.client_socket.listen(0)
            (conn, (_, _)) = self.client_socket.accept()
            client = ClientSocketThread(conn)
            client.start()

TCP_IP = '0.0.0.0'
TCP_PORT = 9099
SERVICE_PORT = 9090
BUFFER_SIZE = 20  # Normally 1024, but we want fast response
if __name__ == '__main__':
    app = App(ip=TCP_IP, port=TCP_PORT, service_ip=TCP_IP, service_port=SERVICE_PORT)
    app.run()
