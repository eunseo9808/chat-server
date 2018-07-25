from .models import Chat, ChatRoom
import datetime
from dateutil.relativedelta import relativedelta


def delete_old_chat():
    time = datetime.datetime.now() - relativedelta(days=7)
    ChatRoom.objects.filter(last_chat_time__lte=time).delete()
    Chat.objects.filter(create_date__lte=time).delete()
