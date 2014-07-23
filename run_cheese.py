
from pydisplay import PyDisplay
from pythread import PyThread
from pyqueue  import pyqueue
import cycheese
import pycheese
import pycallback
import time

#@profile decorator
def demo_callback(cb_typ='CYTHONCB', wait=2, rerun=3):
    """ demo callback as python or cython """
    cbs = {
        'CYTHONCB' : PyThread(cimport=cycheese, target=cycheese.find, args=(pycallback.wap_on_callback,)),
        'PYTOHNCB' : PyThread(cimport=pycheese, target=pycheese.find, args=())
    }
    post = {
        'PYDISPLAY': PyDisplay(pyqueue)
    }

    def run():
        th_q = [post['PYDISPLAY'], cbs[cb_typ]]
        [th.setDaemon(True) for th in th_q]
        [th.start()         for th in th_q]

        for i in range(rerun):
            time.sleep(wait)
            [th.on_stop() for th in th_q]
            print "run %d found %d callback items" %(i, len(post['PYDISPLAY'].on_query()))
            [th.on_restart() for th in th_q]

        [th.join(0.5) for th in th_q]

    try:
        run()
    except:
        raise "demo_callback error"

#@
def demo_parallel_loop(jb_typ='CYNOPARALLEL', n=10, rerun=3):
    """ demo parallel via cython parallel or not """

    jobs = {
        'CYNOPARALLEL' : cycheese.cysumpar_no_parallel(n),
        'CYONPARALLEL' : cycheese.cysumpar_on_parallel(n),
#        'PYNOPARALLEL' : pysumpar.pysumpar_no_parallel(n),
#        'PYONPARALLEL' : pysumpar.pysumpar_on_parallel(n)
        }

    def run():
        print "accumulate sum is %d" %(jobs[jb_typ])

    try:
        run()
    except:
        raise "demo_parallel_loop error"

def main():
    """ doctest """
    demo_callback()
    demo_parallel_loop()

if __name__ == '__main__':
    main()
