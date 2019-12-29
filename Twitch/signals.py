from django.dispatch import receiver
import django.dispatch

from Twitch.models import *


new_frame = django.dispatch.Signal(providing_args=["instance", "live"])


@receiver(new_frame)
def stream_minute_frame_update(sender, instance, live, **kwargs):
    users_updated = []
    points = 0
    if live:
        if (instance.date_created.minute % 5) == 0:
            points += 1
        for user in instance.chatters.all():
            if points > 0:
                user.loyalty_points += points
            user.minutes_watched += 1
            users_updated.append(user)

    if len(users_updated) > 0:
        TwitchUser.objects.bulk_update(users_updated, ['loyalty_points', 'minutes_watched'])
