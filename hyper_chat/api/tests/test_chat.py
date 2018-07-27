from .tests import AuthedTestCase
from ..models import Chat, ChatRoom


class TestChat(AuthedTestCase):

    def setUp(self):
        super(TestChat, self).setUp()

        chatroom = ChatRoom.objects.create(owner_id=self.user_id, opponent_id=self.user_id)
        chatroom.save()
        self.chatroom_id = chatroom.id

        chat = Chat.objects.create(sender_id=self.user_id, receiver_id=self.user_id,
                                   chatroom_id=self.chatroom_id, content="HI, It's Test!!")
        chat.save()
        self.chat_id = chat.id

    def test_00_post(self):
        post_request = {
            'sender_id': self.user_id,
            'receiver_id': self.user_id,
            'content': "Hi, It's Test!!"
        }

        post_response = self.client.post('/api/chatrooms/'+str(self.chatroom_id)+"/chats",
                                         data=post_request, format='json')

        self.assertEqual(post_response.status_code, 201)
        self.assertIn('sender_id', post_response.data)
        self.assertIn('receiver_id', post_response.data)
        self.assertIn('content', post_response.data)
        self.assertIn('chatroom_id', post_response.data)
        self.assertIn('create_time', post_response.data)

    def test_01_get(self):
        get_response = self.client.get('/api/chatrooms/'+str(self.chatroom_id)+"/chats")

        self.assertEqual(get_response.status_code, 200)
        self.assertIn('sender_id', get_response.data[0])
        self.assertIn('receiver_id', get_response.data[0])
        self.assertIn('content', get_response.data[0])
        self.assertIn('chatroom_id', get_response.data[0])
        self.assertIn('create_time', get_response.data[0])

    def test_02_search(self):
        post_request = {
            'query': 'Test'
        }
        search_response = self.client.post('/api/chatrooms/' + str(self.chatroom_id) + "/chats/search",
                                           data=post_request)

        self.assertEqual(search_response.status_code, 200)
        self.assertIn('sender_id', search_response.data[0])
        self.assertIn('receiver_id', search_response.data[0])
        self.assertIn('content', search_response.data[0])
        self.assertIn('chatroom_id', search_response.data[0])
        self.assertIn('create_time', search_response.data[0])

        post_request = {
            'query': 'Hello'
        }
        search_response = self.client.post('/api/chatrooms/' + str(self.chatroom_id) + "/chats/search",
                                           data=post_request)

        self.assertEqual(search_response.status_code, 200)
        self.assertListEqual(search_response.data, [])

    def test_03_get_id(self):
        get_response = self.client.get('/api/chats/'+str(self.chat_id))

        self.assertEqual(get_response.status_code, 200)
        self.assertIn('sender_id', get_response.data)
        self.assertIn('receiver_id', get_response.data)
        self.assertIn('content', get_response.data)
        self.assertIn('chatroom_id', get_response.data)
        self.assertIn('create_time', get_response.data)

    def test_04_put_id(self):
        put_request = {
            'content': "Hello, It's Test!!"
        }
        put_response = self.client.put('/api/chats/'+str(self.chat_id), data=put_request)

        self.assertEqual(put_response.status_code, 200)
        self.assertIn('sender_id', put_response.data)
        self.assertIn('receiver_id', put_response.data)
        self.assertIn('chatroom_id', put_response.data)
        self.assertIn('create_time', put_response.data)
        self.assertEqual("Hello, It's Test!!", put_response.data.get('content'))

    def test_05_delete_id(self):
        delete_response = self.client.delete('/api/chats/'+str(self.chat_id))

        self.assertEqual(delete_response.status_code, 200)
        self.assertIn('message', delete_response.data)
