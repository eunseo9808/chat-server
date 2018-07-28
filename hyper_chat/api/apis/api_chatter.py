from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions

from ..models import Chatter
from ..serializers import ChatterSerializer


class ChatterList(APIView):
    def get(self, request):
        chatters = Chatter.objects.all()
        serializer = ChatterSerializer(chatters, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ChatterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        if request.user.id is None:
            return Response({'Error': 'Unauthorized Error'}, status=status.HTTP_401_UNAUTHORIZED)

        chatter = request.user
        check = False

        if request.data.get('nickname') is not None:
            chatter.nickname = request.data['nickname']
            check = True

        if request.data.get('fcm_reg_id') is not None:
            chatter.fcm_reg_id = request.data['fcm_reg_id']
            check = True

        if check:
            chatter.save()

        serializer = ChatterSerializer(chatter)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        if request.user.id is None:
            return Response({'Error': 'Unauthorized Error'}, status=status.HTTP_401_UNAUTHORIZED)
        chatter = request.user
        chatter.delete()
        return Response({'message': 'Success Delete Chatter'}, status=status.HTTP_200_OK)


class ChatterDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, chatter_id):
        chatter = Chatter.objects.get(id=chatter_id)
        serializer = ChatterSerializer(chatter)
        return Response(serializer.data, status=status.HTTP_200_OK)
