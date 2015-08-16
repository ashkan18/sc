from min_heap import MinHeap

__author__ = 'ashkan'


class EventManager(object):
    def __init__(self):
        self.channels = {}
        self.follow_dict = {}
        self.clients = {}

    def add_client(self, client):
        self.clients[client.id] = client
        self.notify_client(client.id)

    def receive_event(self, event_data):
        if not event_data:
            return
        data_array = event_data.split('|')
        if len(data_array) <= 1:
            print u'Server --> Received unknown data: {}'.format(data_array)
        event_type = data_array[1].strip()
        event_func_name = '{}_event'.format(event_type.lower())

        event_func = getattr(self, event_func_name)
        if event_func:
            event_func(data_array)

    def f_event(self, data_array):
        seq_id = data_array[0]
        from_user_id = data_array[2].strip()
        to_user_id = data_array[3].strip()
        self.channels.setdefault(to_user_id, MinHeap()).push(seq_id, '|'.join(data_array))
        self.follow_dict.setdefault(to_user_id, []).append(from_user_id)
        self.notify_client(to_user_id)

    def u_event(self, data_array):
        seq_id = data_array[0]
        from_user_id = data_array[2].strip()
        to_user_id = data_array[3].strip()

        if to_user_id in self.follow_dict and from_user_id in self.follow_dict[to_user_id]:
            self.follow_dict[to_user_id].remove(from_user_id)

    def b_event(self, data_array):
        seq_id = data_array[0]
        for client_id in self.clients.keys():
            self.channels.setdefault(client_id, MinHeap()).push(seq_id, '|'.join(data_array))
            self.notify_client(client_id)

    def p_event(self, data_array):
        seq_id = data_array[0]
        from_user_id = data_array[2].strip()
        to_user_id = data_array[3].strip()
        self.channels.setdefault(to_user_id, MinHeap()).push(seq_id, '|'.join(data_array))
        self.notify_client(to_user_id)

    def s_event(self, data_array):
        seq_id = data_array[0]
        from_user_id = data_array[2].strip()
        if from_user_id in self.follow_dict:
            for follower_id in filter(lambda x: x in self.clients, self.follow_dict[from_user_id]):
                self.channels.setdefault(follower_id, MinHeap()).push(seq_id, '|'.join(data_array))
                self.notify_client(follower_id)

    def notify_client(self, user_id):
        if user_id in self.clients.keys() and user_id in self.channels:
            client = self.clients[user_id]
            for event in self.channels[user_id]:
                client.send_event(event)