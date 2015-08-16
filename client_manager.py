
__author__ = 'ashkan'


class Client(object):
    def __init__(self, conn):
        self.conn = conn
        self.id = None

    def read_data(self):
        if not self.id:
            self.parse_id()

    def parse_id(self):
        data = self.read_line()
        self.id = data.strip()
        print u'set user id to {}'.format(self.id)

    def read_line(self):
        """read a line from a socket"""
        chars = []
        while True:
            a = self.conn.recv(1)
            chars.append(a)
            if a == "\n" or a == "\r":
                return "".join(chars)

    def send_event(self, event):
        print 'Client send {}'.format(event)
        self.conn.send(event + '\n')
