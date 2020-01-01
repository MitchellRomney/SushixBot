import json
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from Twitch.models import TwitchChatMessage, TwitchUser
from Twitch.functions.api import get_users


class TwitchChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = 'twitch_chat'

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if data["type"] == "message":
            self.save_message(data["data"])

    @staticmethod
    def save_message(message):
        if TwitchUser.objects.filter(twitch_id=message["user_id"]).count() == 0:
            get_users([message["username"], ])

        TwitchChatMessage.objects.create(
            twitch_user=TwitchUser.objects.get(twitch_id=message["user_id"]),
            message=message["message"],
            timestamp=datetime.strptime(message["timestamp"], '%Y-%m-%d %H:%M:%S.%f')
        )
