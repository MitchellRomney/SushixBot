import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

from Twitch.models import FollowEvent, TwitchUser, SubscriptionEvent
from Twitch.functions.api import get_twitch_user


@csrf_exempt
def followers(request):
    if request.method == 'GET':
        if "hub.challenge" in request.GET:
            return HttpResponse(request.GET["hub.challenge"], status=200)

    elif request.method == 'POST':
        body = json.loads(request.body)
        if "data" in body:
            payload = body["data"][0]

            try:
                from_user = TwitchUser.objects.get(twitch_id=payload["from_id"])
            except TwitchUser.DoesNotExist:
                from_user = get_twitch_user(twitch_id=payload["from_id"])

            try:
                to_user = TwitchUser.objects.get(twitch_id=payload["to_id"])
            except TwitchUser.DoesNotExist:
                to_user = get_twitch_user(twitch_id=payload["to_id"])

            if FollowEvent.objects.filter(from_user=from_user, to_user=to_user).count() == 0:
                from_user.loyalty_points += 10
                from_user.save(update_fields=['loyalty_points', ])

            followed_at = datetime.strptime(payload['followed_at'], '%Y-%m-%dT%H:%M:%SZ')

            FollowEvent.objects.create(
                from_user=from_user,
                to_user=to_user,
                followed_at=followed_at
            )

    return HttpResponse(status=204)


@csrf_exempt
def subscriptions(request):
    if request.method == 'GET':
        if "hub.challenge" in request.GET:
            return HttpResponse(request.GET["hub.challenge"], status=200)

    elif request.method == 'POST':
        body = json.loads(request.body)
        if "data" in body:
            payload = body["data"][0]

            print(payload)

            try:
                from_user = TwitchUser.objects.get(twitch_id=payload["event_data"]["user_id"])
            except TwitchUser.DoesNotExist:
                from_user = get_twitch_user(twitch_id=payload["event_data"]["user_id"])

            try:
                to_user = TwitchUser.objects.get(twitch_id=payload["event_data"]["broadcaster_id"])
            except TwitchUser.DoesNotExist:
                to_user = get_twitch_user(twitch_id=payload["event_data"]["broadcaster_id"])

            if SubscriptionEvent.objects.filter(from_user=from_user, to_user=to_user).count() == 0:
                from_user.loyalty_points += 50
                from_user.save(update_fields=['loyalty_points', ])

            subscribed_at = datetime.strptime(payload['event_timestamp'], '%Y-%m-%dT%H:%M:%SZ')

            SubscriptionEvent.objects.create(
                from_user=from_user,
                to_user=to_user,
                subscribed_at=subscribed_at,
                sub_plan=payload["event_data"]["tier"]
            )

    return HttpResponse(status=204)
