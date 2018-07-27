import os
from celery import Celery
from django.conf import settings
from pyfcm import FCMNotification

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hyper_chat.settings')
app = Celery('hyper_chat', backend='redis', broker=settings.BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task
def send_fcm(reg_id, message, sender_id, receiver_id, chatroom_id):
    push_service = FCMNotification(api_key=settings.FCM_APIKEY)
    message_title = "Hyper Chat New Message"
    message_body = message

    data_message = {}
    data_message['sender_id'] = sender_id
    data_message['receiver_id'] = receiver_id
    data_message['chatroom_id'] = chatroom_id

    push_service.notify_single_device(registration_id=reg_id, message_title=message_title,
                                      message_body=message_body, data_message=data_message)


@app.task
def add(x, y):
    return x + y