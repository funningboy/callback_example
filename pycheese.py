import cheese
import threading
from pyasync import *

class PyCheese(threading.Thread):
    """ as Python GIL for C callback,
    NORMALCB : it's a normal callback method via void* ptr return with no py gil
    PYTOHNCB : it's a python callback method via python c api with py gil
    """

    def __init__(self, lock, typ='NORMALCB', async=None):
        super(PyCheese, self).__init__()
        assert(isinstance(async, PyAsync))
        assert(typ in ['NORMALCB', 'PYTOHNCB'])
        self._lock  = lock
        self._typ   = typ
        self._async = async
        self._debug = 1
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

    def on_callback(self, name):
        """ as normal callback """
        try:
            if self._debug:
                print "on_callback : %s" %(name)
            self._async.push(name)
        except IOError:
            raise "NORMALCB Error"

    def on_callback_py(self, name):
        """ as python c api callback """
        try:
            if self._debug:
                print "on_callback_py : %s" %(name)
            self._async.push(name)
        except IOError:
            raise "PYTOHNCB Error"

    def on_stop(self):
        try:
            cheese.on_stop()
        except IOError:
            raise "on_stop Error"

    def on_restart(self):
        try:
            cheese.on_restart()
        except IOError:
            raise "on_restart Error"

