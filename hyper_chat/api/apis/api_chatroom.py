from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import permissions

from ..models import ChatRoom
from ..serializers import ChatRoomSerializer


class ChatRoomList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        my_chat_rooms = ChatRoom.objects.filter(Q(owner=request.user) | Q(opponent=request.user)).order_by('-last_chat_time')
        serializers = ChatRoomSerializer(my_chat_rooms, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        chatroom_filter = ChatRoom.objects.filter(owner_id=request.user.id,
                                                  opponent_id=request.data.get('opponent_id'))
        if chatroom_filter.count() > 0:
            return Response({'Error': 'Already Exist ChatRoom'}, status=status.HTTP_400_BAD_REQUEST)
        
        chatroom_filter = ChatRoom.objects.filter(owner_id=request.data.get('opponent_id'),
                                                  opponent_id=request.user.id)
        if chatroom_filter.count() > 0:
            return Response({'Error': 'Already Exist ChatRoom'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        data['owner_id'] = request.user.id
        serializer = ChatRoomSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatRoomDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, chatroom_id):
        chatroom = ChatRoom.objects.get(id=chatroom_id)
        if not (chatroom.owner.id == request.user.id or chatroom.opponent.id == request.user.id):
            return Response({'Error': 'Unauthorized Error'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ChatRoomSerializer(chatroom)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, chatroom_id):
        chatroom = ChatRoom.objects.get(id=chatroom_id)
        if not (chatroom.owner.id == request.user.id or chatroom.opponent.id == request.user.id):
            return Response({'Error': 'Unauthorized Error'}, status=status.HTTP_401_UNAUTHORIZED)

        chatroom.delete()
        return Response({'message': 'Success Delete Chatroom'}, status=status.HTTP_200_OK)
