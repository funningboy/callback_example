
from pydisplay import *
from pyasync import *
from pycheese import *
import threading
import time

lock = threading.Lock()
pyasync = PyAsync(lock=lock)
th_q = {
    # callback handler for c to python
    'PYCHEESE'  : PyCheese(lock=lock, typ='NORMALCB', async=pyasync),
    # display handler for storing/dumping callback info
    'PYDISPLAY' : PyDisplay(lock=lock, async=pyasync),
    # as async queue
    'PYASYNC'   : pyasync,
    }

def wap_on_callback_py(name):
    """ as a wap interface for py callback """
    global th_q
    th_q['PYCHEESE'].on_callback_py(name)


def main():
    """ doctest """
    global th_q

    # spawn all threads
    [th_i.setDaemon(True) for th_i in th_q.values()]
    [th_i.start() for th_i in th_q.values()]

    for i in xrange(2):
        print "run sequence %d" %(i)
        time.sleep(3)

        # stop all threads
        [th_i.on_stop() for th_i in th_q.values()]
        rst = th_q['PYDISPLAY'].on_query()
        print "found %d items for callback collected" %(len(rst))
        time.sleep(0.1)

        # wake up all threads
        [th_i.on_restart() for th_i in th_q.values()]
        time.sleep(0.1)

    # join all threads
    [th_i.join(timeout=0.5) for th_i in th_q.values()]
    th_q['PYDISPLAY'].on_close()

if __name__ == '__main__':
    main()
