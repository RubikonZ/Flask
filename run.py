from flaskapp import create_app
from twitchio.ext import commands
from requests_oauthlib import OAuth2Session
import json
import os
import threading
import time

# if test_config is None:
#     # Load the instance config, if it exists, when not testing
#     app.config.from_pyfile('config.py', silent=True)
# else:
#     # Load the test config if passed in
#     app.config.from_mapping(test_config)

# ensure the instance folder exists
# try:
#     os.makedirs(app.instance_path)
# except OSError:
#     pass


# CONSTANT VARIABLES
twitch_client_secret = os.environ.get('TWITCH_CLIENT_SECRET')
twitch_client_id = os.environ.get('TWITCH_CLIENT_ID')
twitch_token_url = 'https://id.twitch.tv/oauth2/token'
redirect_uri = 'http://localhost:5000/twitch/callback'


# TWITCH "BOT"
def get_oauth_token():

    with open("storage.json", 'r') as storage_file:
        token = json.load(storage_file)
    print(token['access_token'])
    # if token['status']:
    #     # Must tell flask server to make a refresh token request
    #     twitch = OAuth2Session(twitch_client_id, redirect_uri=redirect_uri)
    #     token = twitch.refresh_token(twitch_token_url,
    #                                  refresh_token=token['refresh_token'],
    #                                  client_id=twitch_client_id,
    #                                  client_secret=twitch_client_secret)
    #     access = token['access_token']
    # else:
    #     access = token['access_token']
    twitch_token = f"oauth:{token['access_token']}"
    return twitch_token


nick = os.environ.get('TWITCH_BOT_NICKNAME')
client_id = os.environ.get('TWITCH_CLIENT_ID')


# Twitch-python
# chat = twitch.Chat(channel='#rubikon', nickname='botrubikot', oauth='...').subscribe(
#     lambda message: print(message.channel, message.user.display_name, message.text))

# TwitchIO implementation
class Bot(commands.Bot):

    def __init__(self, twitch_token):
        print(twitch_token, client_id, nick)
        super().__init__(irc_token=twitch_token, client_id=client_id, nick=nick, prefix='!', initial_channels=['rubikon'])

    # Events don't need decorators when subclassed
    async def event_ready(self):
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        print(f'<{message.author.name}>: {message.content}')
        await self.handle_commands(message)

    # Commands use a different decorator
    @commands.command(name='test')
    async def my_command(self, ctx):
        await ctx.send(f'Hello @{ctx.author.name}!')


    # bot = Bot(get_oauth_token())
    # bot.run()

app = create_app()


def start_twitch_bot():
    # time.sleep(4)
    print('Thread with twitch_bot server starting')
    bot = Bot(get_oauth_token())
    print('Retrieved oauth token to run twitch bot')
    bot.run()


if __name__ == '__main__':
    t1 = threading.Thread(target=start_twitch_bot).start()
    app.run('0.0.0.0', debug=True)

