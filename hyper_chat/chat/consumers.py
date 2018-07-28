import json
import ast
import redis

from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_jwt.settings import api_settings

from api.models import Chat, ChatRoom
from api.serializers import ChatterSerializer
from api.models import Chatter
from hyper_chat.celery import send_fcm
from chat.redis_connect import redis_connector


class ChatConsumer(AsyncWebsocketConsumer):

    def redis_terrify(self, room_connected):
        if room_connected is None:
            room_connected = []
        else:
            room_connected = ast.literal_eval(room_connected.decode('utf-8'))

        return room_connected

    async def connect(self):
        if 'test' in self.scope['subprotocols']:
            from hyper_chat.routing import application
            self.scope = application.__call__(self.scope).scope

        if (self.scope.get('user') is None) or self.scope.get('user').id is None:
            await self.close(401)

        self.chatroom_id = self.scope['url_route']['kwargs']['chatroom_id']
        self.room_group_name = 'chat_%s' % self.chatroom_id
	
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        self.redis = redis_connector
        room_connected = self.redis.get(self.room_group_name)
        room_connected = self.redis_terrify(room_connected)
        if self.scope['user'].id not in room_connected:
            room_connected.append(self.scope['user'].id)
        self.redis.set(self.room_group_name, room_connected)
        await self.accept()

    async def disconnect(self, close_code):
        room_connected = self.redis.get(self.room_group_name)
        room_connected = self.redis_terrify(room_connected)

        room_connected.remove(self.scope['user'].id)

        if len(room_connected) == 0:
            self.redis.delete(self.room_group_name)
        else:
            self.redis.set(self.room_group_name, room_connected)

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']

        chatroom = ChatRoom.objects.get(id=self.chatroom_id)
        if chatroom.owner.id == user.id:
            now_receiver = chatroom.opponent

        else:
            now_receiver = chatroom.owner

        room_connected = self.redis.get(self.room_group_name)
        room_connected = self.redis_terrify(room_connected)

        if now_receiver.id not in room_connected:
            reg_id = now_receiver.fcm_reg_id
            if reg_id is not None:
                send_fcm.delay(reg_id, message, user.id, now_receiver.id, chatroom.id)

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
