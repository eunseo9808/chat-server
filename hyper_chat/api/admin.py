from django.contrib import admin
from .models import Chatter, ChatRoom, Chat
from rest_framework.authtoken.models import Token

# Register your models here.
admin.site.register(Chatter)
admin.site.register(ChatRoom)
admin.site.register(Chat)