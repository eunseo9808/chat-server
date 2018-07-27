from chat.custom_websocket_communicator import CustomWebsocketCommunicator
from chat.consumers import ChatConsumer
from django.test import TestCase
from api.models import Chatter
from api.models import ChatRoom
import pytest
import asyncio
import json


class TestLiveChat(TestCase):

    def test_chat(self):
        user = Chatter.objects.create(username='test1234', nickname='test1234')
        user.set_password('test1234')
        user.save()
        self.user_id = user.id

        login_response = self.client.post('/api/auth', {'username': 'test1234', 'password': 'test1234'})

        self.assertEqual(login_response.status_code, 200)
        self.assertIn('token', login_response.data)
        self.token = login_response.data['token']

        chatroom = ChatRoom.objects.create(owner_id=self.user_id, opponent_id=self.user_id)
        chatroom.save()
        self.chatroom_id = chatroom.id

        async def live_chat():
            communicator = CustomWebsocketCommunicator(ChatConsumer,
                                                       '/ws/chatrooms/'+str(self.chatroom_id)+'/?jwt='+self.token,
                                                       self.chatroom_id)
            connected, subprotocol = await communicator.connect()
            self.assertTrue(connected)

            json_request = {
                "message": "Hello HyperConnect!"
            }

            string_request = json.dumps(json_request)
            await communicator.send_to(text_data=string_request)
            await communicator.disconnect()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(live_chat())
