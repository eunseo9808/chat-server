from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser
from rest_framework_jwt.settings import api_settings
from api.models import Chatter
from urllib.parse import urlsplit, parse_qsl


class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        try:
            query_string = scope['query_string'].decode('utf-8')
            query_string = dict(parse_qsl(urlsplit(query_string).path))
        except :
            scope['user'] = AnonymousUser()

        if 'jwt' in query_string:
            try:
                token_key = query_string['jwt']
                user_info = api_settings.JWT_DECODE_HANDLER(token_key)
                chatter = Chatter.objects.get(id=user_info['user_id'])
                scope['user'] = chatter
            except:
                scope['user'] = AnonymousUser()
        return self.inner(scope)


JWTAuthMiddlewareStack = lambda inner: JWTAuthMiddleware(AuthMiddlewareStack(inner))
