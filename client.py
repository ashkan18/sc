import logging

__author__ = 'ashkan'

import SocketServer


class ClientHandler(SocketServer.StreamRequestHandler):
    """
    This class handles each client connection
    it receives user if from client and sets its own user id from that
    and it keeps the connection open to send later events
    """

    def setup(self):
        SocketServer.StreamRequestHandler.setup(self)
        self.user_id = None

    def handle(self):
        while True:
            user_id = self.rfile.readline().strip()
            if not user_id:
                break

            logging.info(u"New client {} got connected".format(user_id))
            self.user_id = user_id
            self.server.event_manager.add_client(self)

    def send_event(self, event):
        self.wfile.write(event)
        self.wfile.flush()

    def finish(self):
        SocketServer.StreamRequestHandler.finish(self)
        if self.user_id:
            self.server.event_manager.remove_client(self.user_id)


class ClientServer(SocketServer.ThreadingTCPServer):

    @staticmethod
    def create(server_address, event_manager):
        return ClientServer(server_address, ClientHandler, event_manager)

    def __init__(self, server_address, BaseRequestHandler, event_manager):
        self.daemon_threads = True
        self.allow_reuse_address = True
        self.event_manager = event_manager
        SocketServer.ThreadingTCPServer.__init__(self, server_address, BaseRequestHandler)