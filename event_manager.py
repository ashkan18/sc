import logging
import config

__author__ = 'ashkan'


class EventManager(object):
    """
    This class manages the core logic of follower maze
    It maintains a list of current users and a dictionary of followers
    follower dict has user_id as key and list of users id of the followers as value
    it has methods to receive event and inform proper client(s)
    """
    def __init__(self):
        self.clients = {}  # a hash of connected clients, key being user_id and value being client
        self.followers = {}

    def receive_event(self, event):
        """
        This method receives an event string and process it
        it makes sure based on the event, follower's dict and clients are updated
        and then it informs related clients
        :param event: config.EVENT_DELIMITER delimited string of event
        """
        event_fields = event.rstrip().split(config.EVENT_DELIMITER)

        assert len(event_fields) > 1

        event_type = event_fields[1].strip()
        event_func_name = '{}_event'.format(event_type.lower())

        event_func = getattr(self, event_func_name)
        if not event_func:
            raise NotImplementedError

        effected_users = event_func(*event_fields[2:])
        if effected_users:
            self.inform_users(effected_users, event)

    def add_client(self, client):
        """
        Adds a new client to list of clients
        :param client: ClientHandler of this client
        """
        self.clients[client.user_id] = client

    def remove_client(self, user_id):
        """
        Removes a client from the list of existing clients
        :param user_id: user_id of the client we want to remove
        """
        del self.clients[user_id]

    def f_event(self, from_user, to_user):
        """
        Follow event, given a seq id, a type, from user and to user
        it adds from_user to list of followers of to_user
        and then it notifies to_user
        :param from_user: String user id of the follower
        :param to_user: String user id of the followed
        :return: [to_user_id]
        """
        logging.info(u"{} has started following {}".format(from_user, to_user))
        self.followers.setdefault(to_user, set()).add(from_user)
        return [to_user]

    def u_event(self, from_user, to_user):
        """
        unfollow event
        :param from_user: String user id of the follower
        :param to_user: String user id of the followed
        :return: list of users to be notified
        """
        logging.info(u"{} has stopped following {}".format(from_user, to_user))
        if to_user in self.followers:
            self.followers[to_user].discard(from_user)
        return []

    def b_event(self):
        """
        Broadcast event
        :return: list of all current users
        """
        logging.info(u"received a broadcast event")
        return self.clients.keys()

    def p_event(self, from_user, to_user):
        """
        Private message event
        :param from_user: String user id of the sender
        :param to_user: String user id of the receiver
        :return: [to_user_id]
        """
        logging.info(u"{} sent private message to {}".format(from_user, to_user))
        return [to_user]

    def s_event(self, from_user):
        """
        Status update
        :param from_user: String user id of the sender
        :return: list of followers of from_user
        """
        logging.info(u"{} updated status".format(from_user))
        if from_user in self.followers:
            return self.followers[from_user]
        else:
            return []

    def inform_users(self, users, event):
        """
        Given a list of users and an event, this method will
        inform each of the users (if they are known and in list of existing clients)
        :param users: list of users we want to inform
        :param event: String event we want to send to users
        """
        for user_id in filter(lambda x: x in self.clients, users):
            self.clients[user_id].send_event(event)
