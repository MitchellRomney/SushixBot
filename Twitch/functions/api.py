import requests
from ItsSushix.settings import TWITCH_CLIENT_ID, SUSHIX_BEARER_TOKEN
from Twitch.models import *
from Twitch.signals import new_frame


def create_stream_minute_frame(user_id, chatters):
    headers = {'Client-Id': TWITCH_CLIENT_ID}
    response = requests.get(f'https://api.twitch.tv/helix/streams?user_id={user_id}', headers=headers).json()

    live = False
    viewers = 0
    game = None
    if len(response["data"]) > 0:
        for stream in response["data"]:
            live = True if stream["type"] == "live" else False
            game, created = Game.objects.get_or_create(game_id=stream["game_id"])
            viewers = stream["viewer_count"]

    stream_minute_frame = StreamMinuteFrame.objects.create(
        twitch_user=TwitchUser.objects.get(twitch_id=user_id),
        viewers=viewers,
        live=live,
        game=game,
    )
    stream_minute_frame.chatters.add(*chatters)
    new_frame.send(sender=None, instance=stream_minute_frame, live=live)


def fetch_chatters():
    response = requests.get('https://tmi.twitch.tv/group/user/itssushix/chatters').json()
    chatters = []
    for category in response["chatters"]:
        chatters += response["chatters"][category]
    return chatters


def fetch_followers(user_id):
    headers = {
        'Client-Id': TWITCH_CLIENT_ID
    }
    response = requests.get(f'https://api.twitch.tv/helix/users/follows?to_id={user_id}', headers=headers).json()
    return response["total"]


def fetch_subscribers(user_id):
    headers = {
        'Client-Id': TWITCH_CLIENT_ID,
        'Authorization': f'Bearer {SUSHIX_BEARER_TOKEN}'
    }
    response = requests.get(f'https://api.twitch.tv/helix/subscriptions?broadcaster_id={user_id}&first=100', headers=headers).json()
    total = len(response["data"])

    while len(response["data"]) == 100:
        cursor = response["pagination"]["cursor"]
        response = requests.get(f'https://api.twitch.tv/helix/subscriptions?broadcaster_id={user_id}&first=100&after={cursor}', headers=headers).json()
        total += len(response["data"])

    return total - 1


def get_twitch_user(twitch_id=None, username=None):
    url = f'https://api.twitch.tv/helix/users?'
    headers = {
        'Client-Id': TWITCH_CLIENT_ID
    }

    if twitch_id:
        url += f'id={twitch_id}'

    elif username:
        url += f'login={username}&'

    response = requests.get(url, headers=headers).json()
    user = response['data'][0]

    return TwitchUser.objects.create(
        twitch_id=user['id'],
        login=user['login'],
        display_name=user['display_name'],
        type=user['type'],
        broadcaster_type=user['broadcaster_type'],
        description=user['description'],
        profile_image_url=user['profile_image_url'],
        offline_image_url=user['offline_image_url'],
        view_count=user['view_count']
    )


def get_users(username_list):
    existing_twitch_users = list(TwitchUser.objects.all().values_list('twitch_id', flat=True))

    headers = {
        'Client-Id': TWITCH_CLIENT_ID
    }

    page = 100
    total_count = 0
    total_user_count = len(username_list)
    total_users = []

    while total_count != total_user_count:
        url = f'https://api.twitch.tv/helix/users?'

        for username in username_list[(page - 100):page]:
            url += f'login={username}&'
            total_count += 1

        page += 100
        response = requests.get(url, headers=headers).json()
        total_users += response['data']

    arr = []

    for user in total_users:
        if int(user['id']) not in existing_twitch_users:
            arr.append(TwitchUser(
                twitch_id=user['id'],
                login=user['login'],
                display_name=user['display_name'],
                type=user['type'],
                broadcaster_type=user['broadcaster_type'],
                description=user['description'],
                profile_image_url=user['profile_image_url'],
                offline_image_url=user['offline_image_url'],
                view_count=user['view_count']
            ))
        else:
            try:
                existing_user = TwitchUser.objects.get(twitch_id=user['id'])
                existing_user.login = user['login']
                existing_user.display_name = user['display_name']
                existing_user.type = user['type']
                existing_user.broadcaster_type = user['broadcaster_type']
                existing_user.description = user['description']
                existing_user.profile_image_url = user['profile_image_url']
                existing_user.offline_image_url = user['offline_image_url']
                existing_user.view_count = user['view_count']
                existing_user.save()

            except TwitchUser.DoesNotExist:
                pass

    if len(arr) > 0:
        TwitchUser.objects.bulk_create(arr)

    return True

