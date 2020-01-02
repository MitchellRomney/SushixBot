import requests
import json


def followers_webhook():
    url = 'https://api.twitch.tv/helix/webhooks/hub'
    body = json.dumps({
        'hub.callback': 'https://api.sushix.tv/twitch/followers',
        'hub.mode': 'subscriber',
        'hub.topic': 'https://api.twitch.tv/helix/users/follows?first=1&to_id=27626321',
        'hub.lease_seconds': 864000,
    })
    response = requests.post(url, body)
    print(response.status_code)
