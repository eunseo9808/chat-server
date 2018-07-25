from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser
from rest_framework_jwt.settings import api_settings
from api.models import Chatter


class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            try:
                token_name, token_key = headers[b'authorization'].decode().split()
                if token_name == 'Token':
                    user_info = api_settings.JWT_DECODE_HANDLER(token_key)
                    chatter = Chatter.objects.get(id=user_info['user_id'])
                    scope['user'] = chatter
            except:
                scope['user'] = AnonymousUser()
        return self.inner(scope)


JWTAuthMiddlewareStack = lambda inner: JWTAuthMiddleware(AuthMiddlewareStack(inner))
