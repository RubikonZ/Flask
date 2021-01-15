from twitchio.ext import commands
from requests_oauthlib import OAuth2Session
import json
import os

# CONSTANT VARIABLES
twitch_client_secret = os.environ.get('TWITCH_CLIENT_SECRET')
twitch_client_id = os.environ.get('TWITCH_CLIENT_ID')
twitch_token_url = 'https://id.twitch.tv/oauth2/token'
redirect_uri = 'http://localhost:5000/twitch/callback'
nick = os.environ.get('TWITCH_BOT_NICKNAME')
client_id = os.environ.get('TWITCH_CLIENT_ID')


def get_oauth_token():
    """ Function retrieves access token """
    with open("storage.json", 'r') as storage_file:
        token = json.load(storage_file)

    # Must tell flask server to make a refresh token request
    twitch = OAuth2Session(twitch_client_id, redirect_uri=redirect_uri)
    token = twitch.refresh_token(twitch_token_url,
                                 refresh_token=token['refresh_token'],
                                 client_id=twitch_client_id,
                                 client_secret=twitch_client_secret)
    twitch_token = f"oauth:{token['access_token']}"
    with open('storage.json', 'w') as storage_file:
        json.dump(token, storage_file, indent=4, ensure_ascii=False)

    return twitch_token


# TwitchIO implementation
def create_twitch_bot():
    bot = commands.Bot(
        irc_token=get_oauth_token(),
        client_id=client_id,
        nick=nick,
        prefix='!',
        initial_channels=['rubikon'],
    )

    # Events don't need decorators when subclassed
    @bot.event
    async def event_ready():
        print(f'Ready | {bot.nick}')

    @bot.event
    async def event_message(message):
        print(f'<{message.author.name}>: {message.content}')
        await bot.handle_commands(message)

    # Commands use a different decorator
    @bot.command(name='test')
    async def my_command(ctx):
        await ctx.send(f'Hello @{ctx.author.name}!')

    return bot
