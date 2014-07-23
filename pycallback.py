
from pyqueue import pyqueue
import time

def wap_on_callback(name, debug=0, wait=0.1):
    """ as a wap interface for py callback """
    global pyqueue
    try:
        if debug:
            print "wap_on_callback %s" %(name)
        pyqueue.push(name)
        time.sleep(wait)
    except IOError:
        raise "PYTOHNCB Error"


