from rest_framework.views import APIView
from .serializers import UserSerializer, ChatRoomSerializer, ChatSerializer
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
from .models import Chatter, ChatRoom, Chat


# Create your views here.
class ChatterList(APIView):
    def get(self, request):
        if request.user is None :
            return Response({'Error': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        chatters = Chatter.objects.all()
        serializer = UserSerializer(chatters, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatRoomList(APIView):
    def get(self, request):
        my_chat_rooms = ChatRoom.objects.filter(Q(owner=request.user) | Q(opponent=request.user)).order_by('-last_chat_time')
        serializers = ChatRoomSerializer(my_chat_rooms, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        chatroom_filter = ChatRoom.objects.filter(owner_id=request.data.get('owner_id'),
                                                  opponent_id=request.data.get('opponent_id'))
        if chatroom_filter.count() > 0:
            return Response({'Error': 'Already Exist ChatRoom'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ChatRoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatList(APIView):
    def get(self, request, chatroom_id):
        my_chats = Chat.objects.filter(chatroom_id=chatroom_id).order_by('create_time')
        if my_chats.count() <= 0:
            return Response({'Error': 'Not Found Chat in ChatRoom: ' + str(chatroom_id)}, status=status.HTTP_400_BAD_REQUEST)
        serializers = ChatSerializer(my_chats, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request, chatroom_id):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(chatroom_id=chatroom_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatSearch(APIView):
    def post(self, request, chatroom_id):
        query = request.data['query']

        query_chats = Chat.objects.filter(chatroom_id=chatroom_id, content__contains=query).order_by('-create_time')
        serializers = ChatSerializer(query_chats, many=True)

        return Response(serializers.data, status=status.HTTP_200_OK)