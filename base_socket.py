from threading import Thread

__author__ = 'ashkan'


class BaseSocketThread(Thread):
    def __init__(self, ip, port, conn):
        Thread.__init__(self)
        self.running = True
        self.ip = ip
        self.port = port
        self.conn = conn

    def run(self):
        while self.running:
            self.process_connection()
        self.conn.close()

    def process_connection(self):
        raise NotImplementedError

    def read_line(self):
        "read a line from a socket"
        chars = []
        while True:
            a = self.conn.recv(1)
            chars.append(a)
            if a == "\n" or a == "\r":
                return "".join(chars)

    def kill(self):
        self.running = False
