

class PyAsync(object):
    """ as Async fifo """

    def __init__(self, deep=100):
        self._deep  = deep
        self._queue = []
        self._stop  = 0

    @property
    def deep(self):
        return self._deep

    @property
    def queue(self):
        return self._queue

    def push(self, frame):
        if not self._stop:
            self._queue.append(frame)

    def pop(self):
        if not self._stop:
            return self._queue.pop()

    def is_work(self):
        return len(self._queue) > 0

    def on_stop(self):
        self._stop = 1

    def on_restart(self):
        self._stop = 0


