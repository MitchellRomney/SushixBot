import requests
import json


def followers_webhook():
    print('Starting Followers Webhook...')
    url = 'https://api.twitch.tv/helix/webhooks/hub'
    body = json.dumps({
        "hub.callback": "https://api.sushix.tv/twitch/followers",
        "hub.mode": "subscribe",
        "hub.topic": "https://api.twitch.tv/helix/users/follows?first=1&to_id=27626321",
        "hub.lease_seconds": 864000
    })

    headers = {
        "Authorization": "Bearer qrdtg7k3wng14dfvznz0b1l3izgcot"
    }

    print(f'Sending Webhook Request to {url} with body of {body}')
    response = requests.post(url, body, headers)
    print('Followers Webhook Response Code: ' + response.status_code)
