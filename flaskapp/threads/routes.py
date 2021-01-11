from flask import request, Blueprint, redirect, session, url_for, flash, render_template
import threading
from twitch_bot import create_twitch_bot

threads = Blueprint('threads', __name__)


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
        regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self.running = threading.Event()

    def start_app(self):
        self.running.set()

    def stop_app(self):
        self.running.clear()

    def is_running(self):
        if self.running.is_set():
            return "Twitch app is running"
        else:
            return "Twitch app is offline"


def twitch_thread():
    print('twitch thread starting')
    twitch.run()


tw_thread = StoppableThread(target=twitch_thread) # Should be inside "start()" function so that you create new thread object every time
twitch = create_twitch_bot()
thread_running = None


@threads.route("/start")
def start():
    global thread_running
    if thread_running is not None:
        flash('Threads already running', 'info')
        return redirect(url_for('main.home'))

    tw_thread.start_app()
    thread_running = True
    tw_thread.start()
    tw_thread.join()

    # tw_thread.start_app()
    flash('Started twitch thread', 'success')
    return redirect(url_for('main.home'))


@threads.route("/stop")
def stop():
    global thread_running, tw_thread
    if thread_running is None:
        flash('Threads are not running', 'info')
        return redirect(url_for('main.home'))
    thread_running = False
    tw_thread.stop_app()

    flash('Stopped threads', 'success')
    return redirect(url_for('main.home'))

