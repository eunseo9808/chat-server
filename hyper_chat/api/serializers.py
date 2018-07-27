from rest_framework import serializers
from .models import Chatter, ChatRoom, Chat


class ChatterSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Chatter.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user

    class Meta:
        model = Chatter
        fields = ('id', 'username', 'password', 'nickname', )
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
        }


class ChatRoomSerializer(serializers.HyperlinkedModelSerializer):
    owner_id = serializers.IntegerField(write_only=True)
    opponent_id = serializers.IntegerField(write_only=True)
    owner = ChatterSerializer(read_only=True)
    opponent = ChatterSerializer(read_only=True)

    class Meta:
        model = ChatRoom
        fields = ('id', 'owner_id', 'opponent_id', 'last_chat_time', 'create_time', 'owner', 'opponent', )
        read_only_fields = ('id', 'owner', 'opponent', 'last_chat_time', 'create_time', )


class ChatSerializer(serializers.HyperlinkedModelSerializer):
    sender_id = serializers.IntegerField()
    receiver_id = serializers.IntegerField()

    class Meta:
        model = Chat
        fields = ('id', 'chatroom_id', 'sender_id', 'receiver_id', 'content', 'create_time', )
        read_only_fields = ('id', 'create_time',)


