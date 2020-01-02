import requests


def get_current_webhooks():
    url = 'https://api.twitch.tv/helix/webhooks/subscriptions'
    headers = {
        "Authorization": "Bearer qrdtg7k3wng14dfvznz0b1l3izgcot"
    }
    response = requests.get(url, headers=headers).json()
    subscriptions = []

    if response["data"]:
        for key in response["data"]:
            subscription = response["data"][key]
            if subscription["callback"] == "https://api.sushix.tv/twitch/followers":
                subscriptions.append("Followers")

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
        "Authorization": "Bearer qrdtg7k3wng14dfvznz0b1l3izgcot"
    }

    requests.post(url, data=body, headers=headers)
