from base_socket import BaseSocketThread

__author__ = 'ashkan'


class ClientSocketThread(BaseSocketThread):

    def __init__(self, ip, port, conn):
        super(ClientSocketThread, self).__init__(ip=ip, port=port, conn=conn)
        self.user_id = None

    def process_connection(self):
        if not self.user_id:
            data = self.read_line()
            self.parse_user_id(data)

        # we already know the client
        pending_message = self.check_for_messages()
        if pending_message:
            print "Client {}: {}".format(self.user_id, pending_message)
            self.conn.send(pending_message)

    def parse_user_id(self, data):
        self.user_id = data.strip()
        print u'set user id to {}'.format(self.user_id)
        if self.user_id not in channels:
            channels[self.user_id] = []
            follow_dict[self.user_id] = []

    def check_for_messages(self):
        if self.user_id in channels and channels[self.user_id]:
            return channels[self.user_id].pop()
        else:
            # check global messages
            return channels['*']

