import json
import os
import websockets

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
    @commands.command(name='test')
    async def top_points__command(self, ctx):
        message = queries.query_leaderboard
        # top_users = TwitchUser.objects.filter(bot=False).order_by('-loyalty_points')[:10]
        # message = 'Top 10 SushiRolls:'
        # for (user, index) in top_users:
        # message += f' {index + 1}. {user.display_name} ({user.loyalty_points}){i:{"," if index < 9 else ""}}'
        await ctx.send(f'{message}')


if __name__ == '__main__':
    bot = TwitchBot()
    bot.run()
