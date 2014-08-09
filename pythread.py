# -*- coding: utf-8 -*-

import threading
import time

class PyThread(threading.Thread):
    """ as Python threading callback handler """

    def __init__(self, cimport=None, target=None, args=(), kwargs={}):
        threading.Thread.__init__(self, target=target, args=args, kwargs=kwargs)
        self._cimport = cimport
        self._debug = 0

    def on_stop(self, wait=0):
        """ nofity c to do on_stop """
        try:
            self._cimport.on_stop()
            time.sleep(wait)
        except IOError:
            raise "on_stop Error"

    def on_restart(self, wait=0):
        """ notify c to do on_restart """
        try:
            self._cimport.on_restart()
            time.sleep(wait)
        except IOError:
            raise "on_restart Error"


