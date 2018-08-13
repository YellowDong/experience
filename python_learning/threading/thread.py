#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from threading import Event, Thread


def countdown(n, started_evt):
    print('start')
    started_evt.set()
    while n > 0:
        print(n)
        n -= 1
        time.sleep(5)

started_evt = Event()

print('Launching countdown')
t = Thread(target=countdown, args=(10, started_evt))
t.start()
t.join()
started_evt.wait()
print('countdown is running')
