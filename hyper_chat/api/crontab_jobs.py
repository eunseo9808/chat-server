from .models import Chat, ChatRoom
import datetime


def delete_old_chat():
    time = datetime.datetime.now() - datetime.timedelta(days=7)
    ChatRoom.objects.filter(last_chat_time__lte=time).delete()
    Chat.objects.filter(create_date__lte=time).delete()
