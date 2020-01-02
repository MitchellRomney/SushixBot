import json
import os
import websockets
import requests

from dotenv import load_dotenv
from twitchio.ext import commands

import queries


class TwitchBot(commands.Bot):
    def __init__(self):
        load_dotenv()
        self.ws_url = os.getenv("API_WS_URL")
        self.ws = None
        super().__init__(
            irc_token=os.getenv("TWITCH_IRC_TOKEN"),
            client_id=os.getenv("TWITCH_CLIENT_SECRET"),
            nick='SushixBot',
            prefix='!',
            initial_channels=['ItsSushix']
        )

    async def start_websocket(self):
        self.ws = await websockets.connect(self.ws_url)

    async def event_ready(self):
        await self.start_websocket()
        print(f'Ready | {self.nick}')

    async def event_usernotice_subscription(self, metadata):
        print(metadata)

    async def event_message(self, message):
        tags = {}
        for tag in message.raw_data.split(';'):
            tag_split = tag.split('=')
            tag_key = tag_split[0]
            tags[tag_key] = {}
            if len(tag_split) > 1:
                tag_values = tag_split[1].split(',')
                for key in tag_values:
                    if len(key.split('/')) > 1:
                        tag_values_split = key.split('/')
                        tags[tag_key][tag_values_split[0]] = tag_values_split[1]
                    else:
                        tags[tag_key] = key
            else:
                tags[tag_key] = ''

        payload = json.dumps({
            'type': 'message',
            'data': {
                'message': message.content,
                'user_id': message.author.id,
                'username': message.author.name,
                'tags': tags,
                'timestamp': str(message.timestamp)
            }
        })

        try:
            await self.ws.send(payload)
        except websockets.exceptions.ConnectionClosedError:
            await self.start_websocket()
            await self.ws.send(payload)

        await self.handle_commands(message)

    # Commands use a different decorator
    @commands.command(name='top')
    async def top_points__command(self, ctx):
        query = queries.query_leaderboard
        url = 'https://api.sushix.tv/graphql'
        response = requests.post(url, json={
            'query': query,
            'variables': {
                'metric': 'loyaltyPoints'
            }
        }).json()

        message = ''
        position = 0
        leaderboard = response['data']['leaderboard'][:10]

        for user in leaderboard:
            position += 1
            message += f'#{position}. {user["displayName"]} ({user["loyaltyPoints"]})'
            if position != 10:
                message += ', '
        await ctx.send(f'{message}')

    @commands.command(name='points')
    async def points_command(self, ctx):
        query = queries.query_twitch_user
        url = 'https://api.sushix.tv/graphql'
        response = requests.post(url, json={
            'query': query,
            'variables': {
                'username': ctx.author.name
            }
        }).json()

        if "twitchUser" in response['data']:
            user = response['data']['twitchUser']
            message = f'{user["displayName"]}, you have {user["loyaltyPoints"]} Sushi Rolls.'
        else:
            message = 'Cannot find user.'

        await ctx.send(f'{message}')

    @commands.command(name='commands')
    async def commands_command(self, ctx):
        message = 'Available Commands: !top, !points, !ally, !stack, !discord'
        await ctx.send(f'{message}')


if __name__ == '__main__':
    bot = TwitchBot()
    bot.run()
