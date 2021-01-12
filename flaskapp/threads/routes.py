from flask import request, Blueprint, redirect, session, url_for, flash, render_template
import threading
from twitch_bot import create_twitch_bot
import time
from datetime import datetime

threads = Blueprint('threads', __name__)


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
        regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop = threading.Event()  # initially FALSE

    def stop(self):
        print('Stopping thread')
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()  # running if FALSE


name = 'twitch-thread'


def get_stoppable_thread(thread_name):
    all_threads = threading.enumerate()
    for thread in all_threads:
        if thread.getName() == thread_name:  # Works only for single thread (for now)
            print(thread, thread.stopped())
            return thread, thread.stopped()
    return None, None


def twitch_thread():
    print('twitch thread starting')
    twitch.run()


twitch = create_twitch_bot()


@threads.route("/start")
def start():
    thread, thread_not_running = get_stoppable_thread(name)

    if thread_not_running == False:
        flash('Threads already running', 'info')
        return redirect(url_for('main.home'))
    tw_thread = StoppableThread(target=twitch_thread, name=name)
    tw_thread.setDaemon(True)
    tw_thread.start()
    # tw_thread.join()
    flash('Started twitch thread', 'success')
    return redirect(url_for('main.home'))


@threads.route("/stop")
def stop():
    thread, thread_not_running = get_stoppable_thread(name)
    if thread_not_running or thread_not_running is None:
        flash('Threads are not running', 'info')
        return redirect(url_for('main.home'))
    if thread:
        thread.stop()
        flash('Stopped threads', 'success')
        return redirect(url_for('main.home'))
