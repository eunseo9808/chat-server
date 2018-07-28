import datetime

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions

from api.models import ChatRoom, Chat
from api.serializers import ChatSerializer


class ChatList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, chatroom_id):
        chatroom = ChatRoom.objects.get(id=chatroom_id)
        if not (chatroom.owner.id == request.user.id or chatroom.opponent.id == request.user.id):
           return Response({'Error': 'Unauthorized Error'}, status=status.HTTP_401_UNAUTHORIZED)
 
        my_chats = Chat.objects.filter(chatroom_id=chatroom_id).order_by('create_time')
        if my_chats.count() <= 0:
            return Response({'Error': 'Not Found Chat in ChatRoom: ' + str(chatroom_id)},
                            status=status.HTTP_400_BAD_REQUEST)
        serializers = ChatSerializer(my_chats, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request, chatroom_id):
        chatroom = ChatRoom.objects.get(id=chatroom_id)
        if not (chatroom.owner.id == request.user.id or chatroom.opponent.id == request.user.id):
           return Response({'Error': 'Unauthorized Error'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(chatroom_id=chatroom_id, sender_id=request.user.id)

            chatroom = ChatRoom.objects.get(id=chatroom_id)
            chatroom.last_chat_time = datetime.datetime.now()
            chatroom.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, chat_id):
        chat = Chat.objects.get(id=chat_id)
        if not (chat.sender_id == request.user.id or chat.receiver_id == request.user.id):
            return Response({'Error': 'Unauthorized Error'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = ChatSerializer(chat)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, chat_id):
        chat = Chat.objects.get(id=chat_id)
        if not chat.sender_id == request.user.id:
            return Response({'Error': 'Unauthorized Error'}, status=status.HTTP_401_UNAUTHORIZED)

        if request.data.get('content') is not None:
            chat.content = request.data['content']
            chat.save()

        serializer = ChatSerializer(chat)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, chat_id):
        chat = Chat.objects.get(id=chat_id)
        if not chat.sender_id == request.user.id:
            return Response({'Error': 'Unauthorized Error'}, status=status.HTTP_401_UNAUTHORIZED)

        chat.delete()
        return Response({'message': 'Success Delete Chat'}, status=status.HTTP_200_OK)


class ChatSearch(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, chatroom_id):
        chatroom = ChatRoom.objects.get(id=chatroom_id)
        if not (chatroom.owner.id == request.user.id or chatroom.opponent.id == request.user.id):
           return Response({'Error': 'Unauthorized Error'}, status=status.HTTP_401_UNAUTHORIZED)

        query = request.data['query']

        query_chats = Chat.objects.filter(chatroom_id=chatroom_id, content__contains=query).order_by('-create_time')
        serializers = ChatSerializer(query_chats, many=True)

        return Response(serializers.data, status=status.HTTP_200_OK)
