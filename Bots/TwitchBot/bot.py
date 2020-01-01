import json
import os
import websockets
import requests

from dotenv import load_dotenv
from twitchio.ext import commands
from twitchio.webhook import UserFollows

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

    async def event_message(self, message):
        payload = json.dumps({
            'type': 'message',
            'data': {
                'message': message.content,
                'user_id': message.author.id,
                'username': message.author.name,
                'raw': message.raw_data,
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
                'metric': 'loyalty_points'
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


if __name__ == '__main__':
    bot = TwitchBot()
    bot.run()
