from django.dispatch import receiver
from django.utils import timezone
import django.dispatch

from Twitch.models import TwitchUser, TwitchChatMessage

new_frame = django.dispatch.Signal(providing_args=["instance", "live"])


@receiver(new_frame)
def stream_minute_frame_update(sender, instance, live, **kwargs):
    users_updated = []
    active_chatters = []
    points = 0

    if (instance.date_created.minute % 5) == 0 and live:

        # Add 1 loyalty point for being on the stream while live.
        points += 1

        # Get a list of ID's of every user who has sent a message in chat in the last 5 minutes.
        active_chatters = list(TwitchChatMessage.objects
                               .filter(date_created__gt=(timezone.now() + timezone.timedelta(minutes=-5)))
                               .values_list('twitch_user__id', flat=True))

    elif (instance.date_created.minute % 30) == 0 and not live:

        # Add 1 loyalty point for being on the stream while offline.
        points += 1

    for user in instance.chatters.all():
        user_updated = False

        # Add 2 loyalty points if user has been active in the chat.
        if user.id in active_chatters and live:
            points += 2

        if points > 0:
            user.loyalty_points += points
            user_updated = True

        if live:
            user.minutes_watched += 1
            user_updated = True

        if user_updated:
            users_updated.append(user)

    if len(users_updated) > 0:
        TwitchUser.objects.bulk_update(users_updated, ['loyalty_points', 'minutes_watched'])
