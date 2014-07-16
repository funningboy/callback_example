# utf8

from pydisplay import *
from pyasync import *
from pycheese import *
import time

async = PyAsync()

# thread queue
th_q = {
        'PYCHEESE' : PyCheese(async=async),
        'PYDISPLAY': PyDisplay(async=async),
        }

def wap_on_callback_py(name):
    """ as a wap interface for py callback """
    th_q['PYCHEESE'].on_callback_py(name)


def main():
    """ doctest """

    [th_i.setDaemon(True) for th_i in th_q.values()]

    # spawn all threads
    [th_i.start() for th_i in th_q.values()]

    for i in xrange(2):
        print "run %d" %(i)
        time.sleep(1)

        # stop thread
        [th_i.on_stop() for th_i in th_q.values()]
        time.sleep(1)

        # wake up thread
        if i < 1:
            [th_i.on_restart() for th_i in th_q.values()]

    # join all threads
    [th_i.join() for th_i in th_q.values()]

if __name__ == '__main__':
    main()
