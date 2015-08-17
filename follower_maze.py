import logging

__author__ = 'ashkan'

import threading
from client import ClientServer
from event_manager import EventManager
from server import EventServer


class FollowerMaze(object):
    """
    This Class sets up two ports to listen to ONE event sender and Multiple clients
    Each port will run on a separate thread
    """
    def __init__(self, event_port, client_port):
        self.event_manager = EventManager()
        self.client_server = ClientServer.create(('', client_port), self.event_manager)
        self.event_server = EventServer.create(('', event_port), self.event_manager)

    def start(self):
        logging.debug('Start listening on server and client ports...')
        client_thread = threading.Thread(target=self.client_server.serve_forever)
        client_thread.daemon = True
        client_thread.start()

        event_thread = threading.Thread(target=self.event_server.serve_forever)
        event_thread.daemon = True
        event_thread.start()

    def stop(self):
        logging.info('Stop listening on server and client ports...')
        self.client_server.shutdown()
        self.event_server.shutdown()
        del self.client_server
        del self.event_server
