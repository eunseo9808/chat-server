from channels.generic.websocket import AsyncWebsocketConsumer
from api.models import Chat, ChatRoom
import json
from rest_framework_jwt.settings import api_settings
from api.models import Chatter


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chatroom_id = self.scope['url_route']['kwargs']['chatroom_id']
        self.room_group_name = 'chat_%s' % self.chatroom_id

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        token = text_data_json['token']

        user_info = api_settings.JWT_DECODE_HANDLER(token)
        chatter = Chatter.objects.get(id=user_info['user_id'])
        user = chatter

        chatroom = ChatRoom.objects.get(id=self.chatroom_id)
        if chatroom.owner.id == user.id:
            now_receiver = chatroom.opponent

        else:
            now_receiver = chatroom.owner

        chat = Chat.objects.create(sender=user, receiver=now_receiver,
                                   chatroom=chatroom, content=message)
        chat.save()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
