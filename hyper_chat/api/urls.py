from django.urls import path
from django.conf.urls import include

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers

from .apis.api_chatter import ChatterList, ChatterDetail
from .apis.api_chatroom import ChatRoomList, ChatRoomDetail
from .apis.api_chat import ChatList, ChatDetail, ChatSearch


router = routers.DefaultRouter()

urlpatterns = [
    path('chatters', ChatterList.as_view()),
    path('chatters/<int:chatter_id>', ChatterDetail.as_view()),
    path('chatrooms', ChatRoomList.as_view()),
    path('chatrooms/<int:chatroom_id>', ChatRoomDetail.as_view()),
    path('chatrooms/<int:chatroom_id>/chats', ChatList.as_view()),
    path('chatrooms/<int:chatroom_id>/chats/search', ChatSearch.as_view()),
    path('chats/<int:chat_id>', ChatDetail.as_view()),
    path('auth', obtain_jwt_token),
    path('', include(router.urls)),
]
