__author__ = 'ashkan'

class EventManager(object):
    def __init__(self):
        self.channels = {'*': []}
        self.follow_dict = {}

    def receive_event(self, event_data):
        data_array = event_data.split('|')
        if len(data_array) <= 1:
            print u'Server --> Received unknown data: {}'.format(data)
        event_type = data_array[1].strip()
        event_func_name = '{}_event'.format(event_type.lower())

        event_func = getattr(self, event_func_name)
        if event_func:
            event_func(data_array)

    def f_event(self, data_array):
        seq_id = data_array[0]
        from_user_id = data_array[2].strip()
        to_user_id = data_array[3].strip()
        self.channels.setdefault(to_user_id, []).append('{} started following you\n'.format(from_user_id))
        self.follow_dict.setdefault(to_user_id, []).append(from_user_id)

    def u_event(self, data_array):
        seq_id = data_array[0]
        from_user_id = data_array[2].strip()
        to_user_id = data_array[3].strip()

        if to_user_id in self.follow_dict and from_user_id in self.follow_dict[to_user_id]:
            self.follow_dict[to_user_id].remove(from_user_id)

    def b_event(self, data_array):
        seq_id = data_array[0]
        self.channels['*'].append('new broadcast message')

    def p_event(self, data_array):
        seq_id = data_array[0]
        from_user_id = data_array[2].strip()
        to_user_id = data_array[3].strip()
        self.channels.setdefault(to_user_id, []).append(u"{} sent you private message".format(from_user_id))

    def s_event(self, data_array):
        seq_id = data_array[0]
        from_user_id = data_array[2].strip()
        if from_user_id in self.follow_dict:
            for follower_id in self.follow_dict[from_user_id]:
                self.channels.setdefault(follower_id, []).append(u"{} updated status".format(from_user_id))

