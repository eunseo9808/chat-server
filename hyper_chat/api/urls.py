"""hyper_chat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from .views import ChatterList, ChatRoomList, ChatList, ChatSearch
from rest_framework import routers
from django.conf.urls import include


router = routers.DefaultRouter()


urlpatterns = [
    path('chatters', ChatterList.as_view()),
    path('chatrooms', ChatRoomList.as_view()),
    path('chatrooms/<int:chatroom_id>/chats', ChatList.as_view()),
    path('chatrooms/<int:chatroom_id>/chats/search', ChatSearch.as_view()),
    path('auth', obtain_jwt_token),
    path('', include(router.urls))
]
