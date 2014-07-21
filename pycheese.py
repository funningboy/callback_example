import cheese
from pyasync import *

import threading
import time

class PyCheese(threading.Thread):
    """ as Python GIL for C callback,
    NORMALCB : it's a normal callback method via void* ptr return with no py gil
    PYTOHNCB : it's a python callback method via python c api with py gil
    """

    def __init__(self, lock, typ='NORMALCB', async=None):
        threading.Thread.__init__(self)
        assert(isinstance(async, PyAsync))
        assert(typ in ['NORMALCB', 'PYTOHNCB'])
        self._lock  = lock
        self._typ   = typ
        self._async = async
        self._debug = 0
        self._typs  = {
                'NORMALCB' : {
                    'handler' : cheese.find,
                    'args'    : (self.on_callback),
                    },

                'PYTOHNCB' : {
                    'handler' : cheese.find_py,
                    'args'    : None,
                    },
            }

    def run(self):
        """ register callback(report_cheese) to c """
        try:
            handler = self._typs[self._typ]['handler']
            args    = self._typs[self._typ]['args']
            handler(args) if args is not None else handler()
        except IOError:
            raise "%s handler Error" %(self._typ)

    def on_callback(self, name, wait=0.1):
        """ as normal callback """
        try:
            if self._debug:
                print "on_callback : %s" %(name)
            self._async.push(name)
            time.sleep(wait)
        except IOError:
            raise "NORMALCB Error"

    def on_callback_py(self, name, wait=0.1):
        """ as python c api callback """
        try:
            if self._debug:
                print "on_callback_py : %s" %(name)
            self._async.push(name)
            time.sleep(wait)
        except IOError:
            raise "PYTOHNCB Error"

    def on_stop(self, wait=0):
        """ stop """
        try:
            cheese.on_stop()
            time.sleep(wait)
        except IOError:
            raise "on_stop Error"

    def on_restart(self, wait=0):
        """ restart """
        try:
            cheese.on_restart()
            time.sleep(wait)
        except IOError:
            raise "on_restart Error"

