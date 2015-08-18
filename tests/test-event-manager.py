import unittest
from event_manager import EventManager


class MockClient(object):
    """
    Not using unittest.mock since challenge said not use not default libraries
    """
    def __init__(self, user_id):
        self.user_id = user_id

    def send_event(self, message):
        pass


class TestEventManager(unittest.TestCase):
    def setUp(self):
        self.event_manager = EventManager()
        self.client = MockClient(user_id='60')
        self.client2 = MockClient(user_id='50')

    def test_add_client(self):
        self.assertEqual(len(self.event_manager.clients), 0)

        self.event_manager.add_client(self.client)
        self.assertEqual(len(self.event_manager.clients), 1)
        self.assertEqual(self.event_manager.clients[self.client.user_id].user_id, self.client.user_id)

    def test_remove_client(self):
        self.event_manager.clients[self.client.user_id] = self.client
        self.assertEqual(len(self.event_manager.clients), 1)
        self.assertEqual(self.event_manager.clients[self.client.user_id].user_id, self.client.user_id)

        self.event_manager.remove_client(self.client.user_id)
        self.assertEqual(len(self.event_manager.clients), 0)

    def test_wrong_event(self):
        bogus_event = '666\F/60D50'
        with self.assertRaises(AssertionError):
            self.event_manager.receive_event(bogus_event)

    def test_follow_event_no_user(self):
        follow_event = '666|F|60|50'
        self.assertEqual(len(self.event_manager.clients), 0)
        self.assertEqual(len(self.event_manager.followers), 0)
        self.event_manager.receive_event(follow_event)
        self.assertEqual(len(self.event_manager.clients), 0)
        self.assertEqual(len(self.event_manager.followers), 1)
        self.assertIn('50', self.event_manager.followers)
        self.assertIn('60', self.event_manager.followers['50'])

    def test_follow_event_with_user(self):
        follow_event = '666|F|60|50'
        self.event_manager.add_client(self.client)
        self.event_manager.add_client(self.client2)
        self.assertEqual(len(self.event_manager.clients), 2)
        self.assertEqual(len(self.event_manager.followers), 0)
        self.event_manager.receive_event(follow_event)
        self.assertEqual(len(self.event_manager.clients), 2)
        self.assertEqual(len(self.event_manager.followers), 1)
        self.assertIn('50', self.event_manager.followers)
        self.assertIn('60', self.event_manager.followers['50'])

    def test_un_follow(self):
        self.event_manager.followers.setdefault('60', set()).add('50')
        response = self.event_manager.u_event('50', '60')
        self.assertEqual(len(self.event_manager.followers['60']), 0)
        self.assertEqual(len(response), 0)  # no one is informed

    def test_broadcast_event(self):
        self.event_manager.add_client(self.client)
        self.event_manager.add_client(self.client2)
        response = self.event_manager.b_event()
        self.assertEqual(len(response), 2)
        self.assertIn(self.client.user_id, response)
        self.assertIn(self.client2.user_id, response)

    def test_status_event(self):
        self.event_manager.followers.setdefault(self.client.user_id, set()).add(self.client2.user_id)
        response = self.event_manager.s_event(self.client.user_id)
        self.assertEqual(len(response), 1)
        self.assertIn(self.client2.user_id, response)

    def test_send_message_event(self):
        self.event_manager.followers.setdefault(self.client.user_id, set()).add(self.client2.user_id)
        response = self.event_manager.p_event(self.client.user_id, self.client2.user_id)
        self.assertEqual(len(response), 1)
        self.assertIn(self.client2.user_id, response)


if __name__ == '__main__':
    unittest.main()


