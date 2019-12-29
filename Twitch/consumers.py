import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class TwitchChatConsumer(WebsocketConsumer):
    def connect(self):

        self.room_group_name = 'twitch_chat'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        print(text_data)

    def send_notification(self, event):
        message = event['message']
        data = event['data'] if 'data' in event else None

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'data': data
        }))
