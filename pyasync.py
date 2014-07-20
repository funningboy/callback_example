
import threading

class PyAsync(threading.Thread):
    """ as Async fifo """

    def __init__(self, lock):
        super(PyAsync, self).__init__()
        self._lock  = lock
        self._queue = []
        self._stop  = 0

    @property
    def deep(self):
        pass

    @property
    def queue(self):
        return self._queue

    def push(self, frame):
        if not self._stop:
            try:
                self._lock.acquire()
                self._queue.append(frame)
            finally:
                self._lock.release()

    def pop(self):
        frame = None
        if not self._stop:
            try:
                self._lock.acquire()
                frame = self._queue.pop() if len(self._queue) > 0 else None
            finally:
                self._lock.release()
            return frame

    def is_work(self):
        rst = False
        try:
            self._lock.acquire()
            rst = len(self._queue) > 0
        finally:
            self._lock.release()
        return rst

    def on_stop(self):
        self._stop = 1

    def on_restart(self):
        self._stop = 0

    def on_clear(self):
        try:
            self._lock.acquire()
            self._queue = []
        finally:
            self._lock.release()

