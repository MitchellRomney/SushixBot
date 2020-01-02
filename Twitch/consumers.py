import json
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from Twitch.models import TwitchChatMessage, TwitchUser
from Twitch.functions.api import get_twitch_user


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
        try:
            twitch_user = TwitchUser.objects.get(twitch_id=message["user_id"])
        except TwitchUser.DoesNotExist:
            twitch_user = get_twitch_user(twitch_id=message["user_id"])

        update_fields = []

        if "@badge-info" in message["tags"]:
            if "subscriber" in message["tags"]["@badge-info"]:
                twitch_user.subscription_months = message["tags"]["@badge-info"]["subscriber"]
                update_fields.append('subscription_months')

        if "color" in message["tags"]:
            twitch_user.color = message["tags"]["color"]
            update_fields.append('color')

        if len(update_fields) > 0:
            twitch_user.save(update_fields=update_fields)

        TwitchChatMessage.objects.create(
            twitch_user=twitch_user,
            message=message["message"],
            tags=message["tags"],
            timestamp=datetime.strptime(message["timestamp"], '%Y-%m-%d %H:%M:%S.%f')
        )
