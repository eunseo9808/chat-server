from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions

from ..models import Chatter
from ..serializers import UserSerializer


class ChatterList(APIView):
    def get(self, request):
        chatters = Chatter.objects.all()
        serializer = UserSerializer(chatters, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatterDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, chatter_id):
        chatter = Chatter.objects.get(id=chatter_id)
        serializer = UserSerializer(chatter)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, chatter_id):
        if not request.user.id == chatter_id:
            return Response({'Error': 'Not Apply User'}, status=status.HTTP_401_UNAUTHORIZED)

        chatter = request.user

        if request.data.get('nickname') is not None:
            chatter.nickname = request.data['nickname']
            chatter.save()

        serializer = UserSerializer(chatter)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, chatter_id):
        chatter = Chatter.objects.get(id=chatter_id)
        chatter.delete()
        return Response({'message': 'Success Delete Chatter'}, status=status.HTTP_200_OK)

