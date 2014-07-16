
from pyasync import *
import threading
import sqlite3

class PyDisplay(threading.Thread):
    """ as Python GIL for py proc """

    def __init__(self, async=None):
        super(PyDisplay, self).__init__()
        assert(isinstance(async, PyAsync))
        self._async = async
        self._stop  = 0

    def run(self):
        """ do as hex dump/byte dump"""
        try:
            while self._async.is_work() and not self._stop:
                print "%s" %(self._async.pop())
        except Error:
            raise "PyDisplay handler Error"

    def on_stop(self):
        try:
            self._stop = 1
        except Error:
            raise "on_stop Error"

    def on_restart(self):
        try:
            self._stop = 0
        except Error:
            raise "on_restart Error"

    def on_query(self):
        pass

