
from pydisplay import *
from pyasync import *
from pycheese import *
import threading
import time

lock = threading.Lock()
pyasync = PyAsync(lock=lock, deep=100)
th_q = {
    'PYCHEESE'  : PyCheese(lock=lock, typ='NORMALCB', async=pyasync),
    'PYDISPLAY' : PyDisplay(lock=lock, async=pyasync),
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
        print "run %d" %(i)
        time.sleep(3)

        # stop thread
        [th_i.on_stop() for th_i in th_q.values()]
        th_q['PYASYNC'].on_clear()
        rst = th_q['PYDISPLAY'].on_query()
        print len(rst)
        time.sleep(1)

        # wake up thread
        if i < 1:
            [th_i.on_restart() for th_i in th_q.values()]

    # join all threads
    [th_i.join() for th_i in th_q.values()]

if __name__ == '__main__':
    main()
