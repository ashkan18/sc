import socket
from base_socket import BaseSocketThread

__author__ = 'ashkan'


class EventServiceSocketThread(BaseSocketThread):

    def __init__(self, ip, port):
        super(EventServiceSocketThread, self).__init__(ip=ip, port=port, conn=None)
        self.event_service_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.event_service_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.event_service_socket.bind((ip, port))

        print u"Waiting for event service connection..."
        self.event_service_socket.listen(4)
        (self.conn, (service_ip, service_port)) = self.event_service_socket.accept()

    def process_connection(self):
        data = self.read_line()
        print "Server ---> received data: {}".format(data)
        self._parse_data(data)
