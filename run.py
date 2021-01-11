from flaskapp import create_app
import threading
from twitch_bot import create_twitch_bot
from telegram_bot import updater
import time


def flask_thread():
    print('flask thread starting')
    flask.run('0.0.0.0')


def twitch_thread():
    print('twitch thread starting')
    twitch.run()


def telegram_thread():
    updater.start_polling()


twitch = create_twitch_bot()
flask = create_app()


if __name__ == '__main__':
    t1 = threading.Thread(target=flask_thread)
    # t2 = StoppableThread(target=twitch_thread)
    # t3 = threading.Thread(target=telegram_thread)
    t1.start()

    # t3.start()
    # time.sleep(3)
    # t2.start()

    # if t2.is_alive():
    #     print('t2 still running')
    # else:
    #     print('Completed')

    t1.join()
    # t2.join()
    # t3.join()


