from flask import Blueprint, redirect, url_for, flash
import threading
from asyncio import get_event_loop, new_event_loop, set_event_loop, Event, ensure_future, Queue, sleep
from twitch_bot import create_twitch_bot
import time
import flaskapp.auth.routes

threads = Blueprint('threads', __name__)


def create_twitch():
    loop = new_event_loop()
    set_event_loop(loop)
    twitch = create_twitch_bot()

    return twitch


channel = 'rubikon'


class TwitchThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
        regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(TwitchThread, self).__init__(*args, **kwargs)
        self._stop_event = None
        self.twitch = None
        self.queue = None
        self.running_twitch = None
        self.running_queue = None

    def run(self):
        self.twitch = create_twitch()
        self._stop_event = Event()
        self.queue = Queue()
        loop = get_event_loop()
        self.running_twitch = ensure_future(self.twitch_start())
        self.running_queue = ensure_future(self.twitch_send())
        loop.run_until_complete(self._stop_event.wait())
        self.running_queue.cancel()
        self.running_twitch.cancel()
        loop.run_until_complete(self.twitch._ws._websocket.close())
        loop.stop()
        loop.close()

    async def twitch_start(self):
        await self.twitch._ws._connect()
        await self.twitch._ws._listen()

    async def twitch_send(self):
        while not self._stop_event.is_set():
            msg = await self.queue.get()
            await self.twitch.get_channel().send(msg)
            await sleep(10)  # Delay between messages

    def stop(self):
        # Stops twitch thread
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()  # running if FALSE


class DalertsThreadTimer(threading.Timer):
    """ Subclass of Timer to make requests on the loop """
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

    def stop(self):
        self.cancel()


def get_stoppable_thread(thread_name):
    """ Checks if instance of stoppable thread exists (for now with hardcoded name)"""
    output_thread = None
    all_threads = threading.enumerate()
    for thread in all_threads:
        if thread.getName() == thread_name:
            print(f'Got thread: {thread}')
            output_thread = thread
    return output_thread


@threads.route("/start")
def start():
    """ Supposedly should create new thread if it doesn't exist yet (Right now it just starts thread once """
    print(f'Current threads: {threading.enumerate()}')
    for name in ['twitch', 'dalerts']:
        thread = get_stoppable_thread(name)
        if thread:
            if thread.is_alive():
                flash(f'{name} thread is already running', 'info')
        else:
            if name == 'twitch':
                tw_thread = TwitchThread(name=name)
                tw_thread.start()
            elif name == 'dalerts':
                dalerts_thread = DalertsThreadTimer(5, flaskapp.auth.routes.dalerts_json)  # Dalerts request every 5 seconds
                dalerts_thread.name = name
                dalerts_thread.start()
            flash(f'Started {name} thread', 'success')
    print(f'Threads after /start: {threading.enumerate()}')
    return redirect(url_for('main.home'))


@threads.route("/stop")
def stop():
    print(f'Current threads: {threading.enumerate()}')
    for name in ['twitch', 'dalerts']:
        thread = get_stoppable_thread(name)
        if thread:
            if thread.is_alive():
                thread.stop()
                flash(f'Stopped {name} thread', 'success')
        else:
            flash(f'Thread "{name}" is not running', 'info')

    print(f'Threads after /stop: {threading.enumerate()}')  # Still gonna show all threads because it takes time to close/finish them
    return redirect(url_for('main.home'))
