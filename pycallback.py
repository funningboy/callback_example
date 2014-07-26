
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


def wap_on_pthread_callback(debug=0, wait=0.1):
    """ as a wap interface for py c api pthread callback """

    def wap_on_python_thread():
        """ sub loop as thread task """
        print("python nogil thread which is controlled by c pthread")

    import threading
    try:
        threading.Thread(target=wap_on_pthread_callback).start()
    except IOError:
        raise "PYTOHNCB Error"

