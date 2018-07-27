import json
import redis
import ast

from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_jwt.settings import api_settings
from pyfcm import FCMNotification

from api.models import Chat, ChatRoom
from api.serializers import ChatterSerializer
from api.models import Chatter


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
        self.push_service = FCMNotification(api_key=settings.FCM_APIKEY)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        self.pool = redis.ConnectionPool(host=settings.REDIS_HOST_ADDRESS, port=settings.REDIS_HOST_PORT, db=0)
        self.redis = redis.Redis(connection_pool=self.pool)

        room_connected = self.redis.get(self.chatroom_id)
        room_connected = self.redis_terrify(room_connected)

        if self.scope['user'].id not in room_connected:
            room_connected.append(self.scope['user'].id)

        self.redis.set(self.chatroom_id, room_connected)
        await self.accept()

    async def disconnect(self, close_code):
        self.redis = redis.Redis(connection_pool=self.pool)
        room_connected = self.redis.get(self.chatroom_id)
        room_connected = self.redis_terrify(room_connected)

        room_connected.remove(self.scope['user'].id)
        self.redis.set(self.chatroom_id, room_connected)

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

        self.redis = redis.Redis(connection_pool=self.pool)
        room_connected = self.redis.get(self.chatroom_id)
        room_connected = self.redis_terrify(room_connected)

        if now_receiver.id not in room_connected:
            reg_id = now_receiver.fcm_reg_id
            if reg_id is not None:
                message_title = "Hyper Chat New Message"
                message_body = message

                data_message = {}
                data_message['sender'] = user.id
                data_message['receiver'] = now_receiver.id
                data_message['chatroom_id'] = chatroom.id

                self.push_service.notify_single_device(registration_id=reg_id, message_title=message_title,
                                                       message_body=message_body, data_message=data_message)

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
