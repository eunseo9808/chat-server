from django.conf.urls import url
from django.urls import path, include
from . import consumers

websocket_urlpatterns = [
    url(r'^ws/chatrooms/(?P<chatroom_id>\d+)/$', consumers.ChatConsumer),
    #path('ws/chatrooms/<int: chatroom_id>/', consumers.ChatConsumer),
]
