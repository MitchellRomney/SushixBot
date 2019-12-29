import json
import os
import time

import websocket

try:
    import thread
except ImportError:
    import _thread as thread

from dotenv import load_dotenv
from twitchio.ext import commands


class Websocket:

    async def run(self):
        await self.ws.run_forever()

    async def on_message(self, ws, message):
        print(message)

    def __init__(self):
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(
            "ws://localhost:8040/",
            on_message=self.on_message,
        )
        self.ws = ws
        self.run()


class TwitchBot(commands.Bot):
    def __init__(self):
        load_dotenv()
        super().__init__(
            irc_token=os.getenv("TWITCH_IRC_TOKEN"),
            client_id=os.getenv("TWITCH_CLIENT_SECRET"),
            nick='SushixBot',
            prefix='!',
            initial_channels=['ItsSushix']
        )
        self.socket = Websocket()

    async def event_ready(self):
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        payload = json.dumps({
            'type': 'message',
            'data': {
                'message': message.content,
                'user_id': message.author.id,
                'raw': message.raw_data,
                'timestamp': str(message.timestamp)
            }
        })
        self.socket.ws.send(payload)
        await self.handle_commands(message)

    # Commands use a different decorator
    @commands.command(name='test')
    async def my_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.name}!')


if __name__ == '__main__':
    bot = TwitchBot()
    bot.run()
