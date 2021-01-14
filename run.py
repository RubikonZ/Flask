from flaskapp import create_app
import threading
from telegram_bot import updater


def flask_thread():
    print('flask thread starting')
    flask.run('0.0.0.0')


def telegram_thread():
    updater.start_polling()


flask = create_app()


if __name__ == '__main__':
    t1 = threading.Thread(target=flask_thread, name='flask-thread')
    # # t3 = threading.Thread(target=telegram_thread)
    t1.start()

    # t3.join()


