__author__ = 'ashkan'


class EventReceiver(object):
    def __init__(self, conn, event_manager):
        self.conn = conn
        self.event_manager = event_manager

    def read_data(self):
        data = self.read_line()
        self.event_manager.receive_event(data)

    def read_line(self):
        """read a line from a socket"""

        chars = []
        while True:
            a = self.conn.recv(1)
            chars.append(a)
            if a == "\n" or a == "\r":
                return "".join(chars).strip()