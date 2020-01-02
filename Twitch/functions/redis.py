import redis
import requests
import pytz

from ItsSushix import settings
from django.utils import timezone
from datetime import timedelta, datetime


def get_new_oath_key():
    client_id = settings.TWITCH_CLIENT_ID
    client_secret = settings.TWITCH_CLIENT_SECRET
    url = f'https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials'
    response = requests.post(url).json()
    expire_datetime = timezone.now() + timedelta(seconds=response['expires_in'])
    redis.StrictRedis().hmset('app_oauth_key', {'token': response['access_token'], 'expires': str(expire_datetime)})
    return {'token': response['access_token'], 'expires': str(expire_datetime)}


def get_app_oath_key():
    r = redis.StrictRedis()
    bytes_key = r.hgetall('app_oauth_key')

    if not bytes_key:
        key = get_new_oath_key()
    else:
        key = {y.decode('ascii'): bytes_key.get(y).decode('ascii') for y in bytes_key.keys()}
        if pytz.utc.localize(datetime.strptime(key['expires'][:-6], '%Y-%m-%d %H:%M:%S.%f')) < timezone.now():
            key = get_new_oath_key()

    return key['token']
