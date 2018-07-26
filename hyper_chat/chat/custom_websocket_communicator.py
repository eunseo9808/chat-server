from channels.testing import WebsocketCommunicator


class CustomWebsocketCommunicator(WebsocketCommunicator):
    def __init__(self, application, path, chatroom_id, headers=None, subprotocols=None):
        super().__init__(application, path, headers, subprotocols)
        self.scope['url_route'] = {
            'kwargs': {
                'chatroom_id': chatroom_id
            }
        }
