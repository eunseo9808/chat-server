import redis
from django.conf import settings

redis_url = settings.REDIS_URL.replace('redis://h:', '')
redis_info, redis_port = redis_url.split(':')
redis_password, redis_host = redis_info.split('@')

redis_connector = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password)
