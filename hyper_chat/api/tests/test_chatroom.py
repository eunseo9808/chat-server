from .tests import AuthedTestCase
from ..models import ChatRoom


class TestChatRoom(AuthedTestCase):

    def setUp(self):
        super(TestChatRoom, self).setUp()

        chatroom = ChatRoom.objects.create(owner_id=self.user_id, opponent_id=self.user_id)
        chatroom.save()
        self.chatroom_id = chatroom.id

    def test_00_post(self):
        chatroom = ChatRoom.objects.get(id=self.chatroom_id)
        chatroom.delete()

        post_request = {
            'opponent_id': self.user_id
        }

        post_response = self.client.post('/api/chatrooms', data=post_request, format='json')

        self.assertEqual(post_response.status_code, 201)
        self.assertIn('owner', post_response.data)
        self.assertIn('opponent', post_response.data)
        self.assertIn('last_chat_time', post_response.data)
        self.assertIn('create_time', post_response.data)

        post_response = self.client.post('/api/chatrooms', data=post_request, format='json')
        self.assertEqual(post_response.status_code, 400)

    def test_01_get(self):
        chatroom = ChatRoom.objects.create(owner_id=self.user_id, opponent_id=self.user_id)
        chatroom.save()

        get_response = self.client.get('/api/chatrooms')

        self.assertEqual(get_response.status_code, 200)
        self.assertIn('owner', get_response.data[0])
        self.assertIn('opponent', get_response.data[0])
        self.assertIn('last_chat_time', get_response.data[0])
        self.assertIn('create_time', get_response.data[0])

    def test_02_get_id(self):
        get_response = self.client.get('/api/chatrooms/'+str(self.chatroom_id))

        self.assertEqual(get_response.status_code, 200)
        self.assertIn('owner', get_response.data)
        self.assertIn('opponent', get_response.data)
        self.assertIn('last_chat_time', get_response.data)
        self.assertIn('create_time', get_response.data)

    def test_03_delete_id(self):
        delete_response = self.client.delete('/api/chatrooms/'+str(self.chatroom_id))

        self.assertEqual(delete_response.status_code, 200)
        self.assertIn('message', delete_response.data)
