__author__ = 'ashkan'


class EventReceiver(object):
    CRLF = "\r\n"

    def __init__(self, conn, event_manager):
        self.conn = conn
        self.event_manager = event_manager
        self.file = self.conn.makefile("rb")

    def read_data(self):
        data = self.read_line()
        self.event_manager.receive_event(data)

    def read_line(self):
        """read a line from a socket"""
        s = self.file.readline()
        if not s:
            return None
        if s[-2:] == self.CRLF:
            s = s[:-2]
        elif s[-1:] in self.CRLF:
            s = s[:-1]
        return s