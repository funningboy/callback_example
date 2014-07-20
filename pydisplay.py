
from pyasync import *
from pyerror import *
import threading
import sqlite3
import os
import time

class PyDisplay(threading.Thread):
    """ as Python GIL for py proc """

    def __init__(self, lock, async=None):
        super(PyDisplay, self).__init__()
        assert(isinstance(async, PyAsync))
        self._lock  = lock
        self._async = async
        self._stop  = 0
        self._debug = 0
        if os.path.exists('example.db'):
            os.remove('example.db')
        self._conn = sqlite3.connect('example.db', check_same_thread=False)
        self._exc  = self._conn.cursor()
        self._exc.execute('CREATE TABLE test \
                             (name text)')
        self._conn.commit()

    def run(self):
        """ do as hex dump/byte dump"""
        try:
            while True:
                if not self._async.is_work():
                    continue
                frame = self._async.pop()
                if self._debug:
                    print "%s" %(frame)
                self._exc.execute("INSERT INTO test VALUES \
                        (\'%s\')" %(frame))
                self._conn.commit()
        except PyError:
            raise "PyDisplay handler Error"

    def join(self):
        self._conn.close()

    def on_stop(self):
        try:
            self._stop = 1
        except PyError:
            raise "on_stop Error"

    def on_restart(self):
        try:
            self._stop = 0
            self._exc.execute('DROP TABLE test')
            self._conn.commit()
            self._exc.execute('CREATE TABLE \
                    test (name, text)')
            self._conn.commit()
        except PyError:
            raise "on_restart Error"

    def on_query(self):
        try:
            rows = self._exc.execute('SELECT * FROM test')
            self._conn.commit()
            rst = rows.fetchall()
            return rst
        except PyError:
            raise "on_query Error"
