from SushixBot.celery import app
from Twitch.functions.api import fetch_chatters, get_users, create_stream_minute_frame
from Twitch.models import *


@app.task
def fetch_stream_state():
    chatters = fetch_chatters()

    new_chatters = []
    existing_chatters = TwitchUser.objects.filter(login__in=chatters).values_list('login', flat=True)

    for user_name in chatters:
        if user_name not in existing_chatters:
            new_chatters.append(user_name)

    if len(new_chatters) > 0:
        get_users(new_chatters)

    create_stream_minute_frame('27626321', TwitchUser.objects.filter(login__in=chatters))

