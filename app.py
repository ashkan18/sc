from select import select
import socket
from client_manager import Client
from event_manager import EventManager
from event_receiver import EventReceiver


class App(object):
    def __init__(self, ip, port, service_ip, service_port):
        self.event_service_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.event_service_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.event_service_socket.bind((service_ip, service_port))
        self.event_service_socket.listen(1)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.bind((ip, port))
        self.client_socket.listen(5)

        self.event_service = None
        self.event_manager = EventManager()

    def run(self):
        connection_client_map = {}

        while True:
            possible_read_sockets = [self.client_socket, self.event_service_socket] + connection_client_map.keys()
            if self.event_service:
                possible_read_sockets.append(self.event_service.conn)

            readable, writable, exceptional = select(possible_read_sockets, [], [])

            for readable_socket in readable:
                if readable_socket == self.event_service_socket and not self.event_service:
                    # received a server connection
                    event_connection, (_, _) = readable_socket.accept()
                    self.event_service = EventReceiver(event_connection, self.event_manager)

                elif readable_socket == self.client_socket:
                    # received a client connection
                    new_client_conn, (_, _) = self.client_socket.accept()
                    client = Client(new_client_conn)
                    connection_client_map[new_client_conn] = client

                elif self.event_service and readable_socket == self.event_service.conn:
                    # received new event
                    self.event_service.read_data()

                elif readable_socket in connection_client_map:
                    # received data from a client
                    connection_client_map[readable_socket].read_data()
                    self.event_manager.add_client(connection_client_map[readable_socket])

TCP_IP = '0.0.0.0'
TCP_PORT = 9099
SERVICE_PORT = 9090
BUFFER_SIZE = 20  # Normally 1024, but we want fast response
if __name__ == '__main__':
    app = App(ip=TCP_IP, port=TCP_PORT, service_ip=TCP_IP, service_port=SERVICE_PORT)
    app.run()
