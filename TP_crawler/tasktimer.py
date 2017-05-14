# -*- encoding: utf-8 -*-
# test access to the ISTEX API
#  author: JC Moissinac (c) 2016 inspired by J.F.Sebastian

from threading import Event, Thread

def call_repeatedly(interval, func, *args):
    stopped = Event()
    def loop():
        internalstop = False
        while (not stopped.wait(interval)) and (not internalstop): # the first call is in `interval` secs
            internalstop = func(*args)
    Thread(target=loop).start()
    return stopped.set

# The event is used to stop the repetitions:
# cancel_future_calls = call_repeatedly(5, print, "Hello, World")
# do something else here...
# cancel_future_calls() # stop future calls

