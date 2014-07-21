
from pydisplay import *
from pyasync import *
from pycheese import *
import threading
import time

ASYNC = 'QUEUE'

lock = threading.Lock()
pyasync = PyQueue() if ASYNC == 'QUEUE' else PyAsync(lock=lock)
th_q = {
    # callback handler for c to python
    'PYCHEESE'  : PyCheese(lock=lock, typ='PYTOHNCB', async=pyasync),
    # display handler for storing/dumping callback info
    'PYDISPLAY' : PyDisplay(lock=lock, async=pyasync),
    # async queue via threading list
    'PYASYNC'   : None if ASYNC == 'QUEUE' else pyasync,
}


def wap_on_callback_py(name, debug=1, wait=0.1):
    """ as a wap interface for py callback """
    try:
        if debug:
            print "on_callback_py : %s" %(name)
        async.push(name)
        #?????
    except IOError:
        raise "PYTOHNCB Error"


def main():
    """ doctest """
    global th_q

    # spawn all threads
    [th_i.setDaemon(True) for th_i in th_q.values() if th_i != None]
    [th_i.start() for th_i in th_q.values() if th_i != None]

    for i in xrange(2):
        print "run sequence %d" %(i)
        time.sleep(3)

        # stop all threads
        [th_i.on_stop() for th_i in th_q.values() if th_i != None]
        rst = th_q['PYDISPLAY'].on_query()
        print "found %d items for callback collected" %(len(rst))
        time.sleep(0.1)

        # wake up all threads
        [th_i.on_restart() for th_i in th_q.values() if th_i != None]
        time.sleep(0.1)

    # join all threads
    [th_i.join(timeout=0.5) for th_i in th_q.values() if th_i != None]
    th_q['PYDISPLAY'].on_close()

if __name__ == '__main__':
    main()
