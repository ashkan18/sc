import logging
import config

__author__ = 'ashkan'


import heapq
import SocketServer


class EventHandler(SocketServer.StreamRequestHandler):
    """
    This is event receiver class, this handles incoming events
    it receives each event and uses min heap to create a proiority queue where
    events are ordered in the queue with sequence id

    once we have proper list of events it sends them to event manager to process
    """

    def setup(self):
        SocketServer.StreamRequestHandler.setup(self)
        self.event_buffer = []
        self.current_seq_id = 1

    def handle(self):
        while True:
            # read and store event *as is* for notification
            event = self.rfile.readline()
            if not event:
                break

            assert config.EVENT_DELIMITER in event
            assert len(event.split(config.EVENT_DELIMITER)) >= 1

            seq_id = int(event.rstrip().split(config.EVENT_DELIMITER)[0])
            logging.debug(u"Received event({}): {}".format(seq_id, event))
            self.__add_new_event(seq_id, event)
            self.__consume_events()

    def __add_new_event(self, seq_id, event):
        # event buffer is a min heap queue
        # add received event to heap using seq id
        heapq.heappush(self.event_buffer, (seq_id, event))

    def __consume_events(self):
        # check top of queue for next event, and pop until we can't find the next event
        while(self.event_buffer
              and self.event_buffer[0][0] == self.current_seq_id):
            _, event = heapq.heappop(self.event_buffer)
            self.server.event_manager.receive_event(event)
            self.current_seq_id += 1


class EventServer(SocketServer.TCPServer):

    @staticmethod
    def create(server_address, event_manager):
        return EventServer(server_address, EventHandler, event_manager)

    def __init__(self, server_address, RequestHandlerClass, event_manager):
        self.allow_reuse_address = True
        self.event_manager = event_manager
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)