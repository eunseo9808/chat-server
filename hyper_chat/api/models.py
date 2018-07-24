from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Chatter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, default="Chatter")

    def __str__(self):
        return self.user.__str__()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Chatter.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.chatter.save()


class ChatRoom(models.Model):
    owner = models.ForeignKey(Chatter, related_name="owner_chat_rooms", on_delete=models.CASCADE)
    opponent = models.ForeignKey(Chatter, related_name="opponent_chat_rooms", on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    last_chat_time = models.DateTimeField(auto_now_add=True)


class Chat(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(Chatter, related_name='sender_chats', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Chatter, related_name='receiver_chats', on_delete=models.CASCADE)
    content = models.TextField(null=False)
    create_time = models.DateTimeField(auto_now_add=True)
