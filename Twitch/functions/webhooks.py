import requests

from Twitch.functions.redis import get_app_oath_key


def get_current_webhooks():
    url = 'https://api.twitch.tv/helix/webhooks/subscriptions'
    headers = {
        "Authorization": f"Bearer {get_app_oath_key()}"
    }
    response = requests.get(url, headers=headers).json()
    subscriptions = []

    if response["data"]:
        print(response["data"])
        for subscription in response["data"]:
            if subscription["callback"] == "https://api.sushix.tv/twitch/followers":
                subscriptions.append("Followers")
            if subscription["callback"] == "https://api.sushix.tv/twitch/subscriptions":
                subscriptions.append("Subscriptions")

    return subscriptions


def subscribe_followers_webhook():
    url = 'https://api.twitch.tv/helix/webhooks/hub'
    body = {
        "hub.callback": "https://api.sushix.tv/twitch/followers",
        "hub.mode": "subscribe",
        "hub.topic": "https://api.twitch.tv/helix/users/follows?first=1&to_id=27626321",
        "hub.lease_seconds": 864000
    }

    headers = {
        "Authorization": f"Bearer {get_app_oath_key()}"
    }

    requests.post(url, data=body, headers=headers)


def subscribe_subscriptions_webhook():
    url = 'https://api.twitch.tv/helix/webhooks/hub'
    body = {
        "hub.callback": "https://api.sushix.tv/twitch/subscriptions",
        "hub.mode": "subscribe",
        "hub.topic": "https://api.twitch.tv/helix/subscriptions/events?broadcaster_id=27626321&first=1",
        "hub.lease_seconds": 864000
    }

    headers = {
        "Authorization": f"Bearer {get_app_oath_key()}"
    }

    requests.post(url, data=body, headers=headers)
