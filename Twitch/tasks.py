from celery.signals import celeryd_init

from ItsSushix.celery import app
from Twitch.functions.api import fetch_chatters, get_users, create_stream_minute_frame, fetch_followers, fetch_subscribers
from Twitch.functions.webhooks import subscribe_followers_webhook, get_current_webhooks
from Twitch.models import TwitchUser


@celeryd_init.connect
def app_start(sender=None, conf=None, **kwargs):

    # Clean out old queue
    app.control.purge()

    check_webhooks.delay()


@app.task
def check_webhooks():
    existing_webhooks = get_current_webhooks()

    if "Followers" not in existing_webhooks:
        subscribe_followers_webhook()


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


@app.task
def fetch_stats():
    followers = fetch_followers('27626321')
    subscribers = fetch_subscribers('27626321')
    user = TwitchUser.objects.get(display_name='ItsSushix')
    user.follower_count = followers
    user.subscriber_count = subscribers
    user.save()
