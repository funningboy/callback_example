
""" default use asyc Queue to handle multi thread shared data """

import threading
import Queue

class PyAsync(threading.Thread):
    """ as Async fifo """

    def __init__(self, lock):
        threading.Thread.__init__(self)
        self._lock  = lock
        self._queue = []
        self._stop  = 0

    @property
    def queue(self):
        """ mutex queue """
        return self._queue

    def push(self, frame):
        """ mutex push """
        if not self._stop:
            try:
                self._lock.acquire()
                self._queue.append(frame)
            finally:
                self._lock.release()

    def pop(self):
        """ mutex pop """
        frame = None
        if not self._stop:
            try:
                self._lock.acquire()
                frame = self._queue.pop(0) if len(self._queue) > 0 else None
            finally:
                self._lock.release()
            return frame

    def is_work(self):
        """ mutex is_work """
        rst = False
        try:
            self._lock.acquire()
            rst = len(self._queue) > 0
        finally:
            self._lock.release()
        return rst

    def on_stop(self):
        """ mutex stop """
        self._stop = 1
        self.on_clear()

    def on_restart(self):
        """ mutex restart """
        self._stop = 0

    def on_clear(self):
        """ mutex clear """
        try:
            self._lock.acquire()
            self._queue = []
        finally:
            self._lock.release()


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

