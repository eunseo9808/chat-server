from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import (BaseUserManager,AbstractBaseUser)
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings


class AccountManager(BaseUserManager):

    def create_user(self, username, password=None):
        user = self.model(
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user


class Chatter(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    nickname = models.CharField(max_length=100, unique=True)

    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin

    def has_module_perms(self, app_label):
        if self.is_active and self.is_superuser:
            return True
        return self.is_admin

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True
        return self.is_admin

    def get_short_name(self):
        return self.nickname


class ChatRoom(models.Model):
    owner = models.ForeignKey(Chatter, related_name="owner_chat_rooms", on_delete=models.CASCADE)
    opponent = models.ForeignKey(Chatter, related_name="opponent_chat_rooms", on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    last_chat_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.owner.__str__() + " AND " + self.opponent.__str__() + " Room"


class Chat(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(Chatter, related_name='sender_chats', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Chatter, related_name='receiver_chats', on_delete=models.CASCADE)
    content = models.TextField(null=False)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.__str__() + " -> "+self.receiver.__str__()+": " + self.content