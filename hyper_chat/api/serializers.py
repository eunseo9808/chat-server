from rest_framework import serializers
from .models import Chatter, ChatRoom, Chat


class UserSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Chatter.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user

    class Meta:
        model = Chatter
        fields = ('id', 'username','password', 'nickname')
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
        }


class ChatRoomSerializer(serializers.HyperlinkedModelSerializer):
    owner_id = serializers.IntegerField(write_only=True)
    opponent_id = serializers.IntegerField(write_only=True)
    owner = UserSerializer(read_only=True)
    opponent = UserSerializer(read_only=True)

    def create(self, validated_data):
        chatroom = ChatRoom.objects.create(**validated_data)
        chatroom.save()

        return chatroom

    class Meta:
        model = ChatRoom
        fields = ('id', 'owner_id', 'opponent_id', 'last_chat_time', 'create_time', 'owner', 'opponent')
        read_only_fields = ('id', 'owner', 'opponent', 'last_chat_time', 'create_time')


class ChatSerializer(serializers.HyperlinkedModelSerializer):
    sender_id = serializers.IntegerField(write_only=True)
    receiver_id = serializers.IntegerField(write_only=True)
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    def create(self, validated_data):
        chat = Chat.objects.create(**validated_data)
        chat.save()

        return chat

    class Meta:
        model = Chat
        fields = ('chatroom_id', 'sender_id', 'receiver_id', 'content', 'create_time', 'sender', 'receiver')
        read_only_fields = ('create_time', 'sender', 'receiver')

