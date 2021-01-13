from flask import request, Blueprint, redirect, session, url_for, flash, render_template
import threading
from twitch_bot import create_twitch_bot
import flaskapp.auth.routes

threads = Blueprint('threads', __name__)


def twitch_thread():
    print('twitch thread starting')
    twitch.run()


twitch = create_twitch_bot()
name = 'twitch-thread'


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
        regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()  # initially FALSE

    def stop(self):
        print('Stopping thread')
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.isSet()  # running if FALSE


class DalertsThreadTimer(threading.Timer):
    """ Subclass of Timer to make requests on the loop """
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


def get_stoppable_thread(thread_name):
    """ Checks if instance of stoppable thread exists (for now with hardcoded name)"""
    all_threads = threading.enumerate()
    print(all_threads)
    for thread in all_threads:
        if thread.getName() == thread_name:  # Works only for single thread (for now)
            print(thread, thread.stopped())
            return thread, thread.stopped()
    return None, None  # Find out what's the best way to get the same return


@threads.route("/start")
def start():
    """ Supposedly should create new thread if it doesn't exist yet (Right now it just starts thread once """
    thread, thread_not_running = get_stoppable_thread(name)
    if thread:
        if thread.is_alive():
            flash('Threads already running', 'info')
            return redirect(url_for('main.home'))
        thread.stop_event.clear()
    else:
        tw_thread = StoppableThread(target=twitch_thread, name=name) #
        dalerts_thread = DalertsThreadTimer(5, flaskapp.auth.routes.dalerts_json) # Dalerts request every 5 seconds
        tw_thread.start()
        dalerts_thread.start()
        # dalerts_thread.join()
        # tw_thread.join()
        flash('Started twitch thread', 'success')
        return redirect(url_for('main.home'))


@threads.route("/stop")
def stop():
    thread, thread_not_running = get_stoppable_thread(name)
    # if thread_not_running or thread_not_running is None:
    #     flash('Threads are not running', 'info')
    #     return redirect(url_for('main.home'))
    if thread:
        if thread.is_alive():
            thread.stop()
            thread.stopped()
            flash('Stopped threads', 'success')
            return redirect(url_for('main.home'))
    else:
        flash('Threads are not running', 'info')
        return redirect(url_for('main.home'))
