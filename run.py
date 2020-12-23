from flaskapp import create_app
import threading
import twitch_bot as tb


def start_twitch_bot():
    # time.sleep(4)
    print('Thread with twitch_bot server starting')

    print('Retrieved oauth token to run twitch bot')
    bot.run()


def start_flask_server():
    app.run('0.0.0.0')


bot = tb.Bot(tb.get_oauth_token())
app = create_app()


if __name__ == '__main__':
    t1 = threading.Thread(target=start_flask_server, args=())
    t2 = threading.Thread(target=start_twitch_bot, args=())
    t1.start()
    t2.start()
    t1.join()
    t2.join()
