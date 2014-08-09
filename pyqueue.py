# -*- coding: utf-8 -*-

import Queue

class PyQueue(Queue.Queue, object):
    """ as Async fifo """

    def __init__(self):
        super(PyQueue, self).__init__()
        self._stop = 0

    def push(self, frame):
        """ mutex push """
        if not self._stop:
            self.put(frame)

    def pop(self):
        """ mutex pop """
        if not self._stop:
            return self.get()

    def is_work(self):
        """ mutex is_work """
        return self.qsize() > 0

    def on_stop(self):
        """ mutex stop """
        self._stop = 1
        self.on_clear()

    def on_restart(self):
        """ mutex restart """
        self._stop = 0

    def on_clear(self):
        """ mutex clear """
        for i in range(self.qsize()):
            self.get()

pyqueue = PyQueue()

