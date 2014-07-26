
from pydisplay import PyDisplay
from pythread import PyThread
from pyqueue  import pyqueue
from profile import profile
import ccycheese
import cpycheese
import cpypthread
import pycallback
import time
from pyerror import PyError


def demo_callback(wait=2, rerun=3):
    """ demo callback as python or cython """
    th_q = []
    cbs = {
            'CYTHONCB' : None,
            'PYTOHNCB' : None
    }
    post = {
            'PYDISPLAY' : None
    }

    def ini(cb_typ):
        """ construct test case """
        global th_q
        cbs.update({
            'CYTHONCB' : PyThread(cimport=ccycheese, target=ccycheese.find, args=(pycallback.wap_on_callback,)),
            'PYTOHNCB' : PyThread(cimport=cpycheese, target=cpycheese.find, args=())
        })
        post.update({
            'PYDISPLAY': PyDisplay(pyqueue)
        })

        th_q = [post['PYDISPLAY'], cbs[cb_typ]]
        [th.setDaemon(True) for th in th_q]
        [th.start()         for th in th_q]
        print "run %s" %(cb_typ)

    def run():
        """ run test case """
        global th_q
        for i in range(rerun):
            time.sleep(wait)
            # stop before join
            [th.on_stop() for th in th_q]
            rst = post['PYDISPLAY'].on_query()

            print "item %d found %d callback items" %(i, len(rst))
            if rst[0:2]:
                print "      first two items [%s]" %(','.join([j[0] for j in rst[0:2]]))

            if i < rerun -1:
                # restart if not last run
                time.sleep(wait)
                [th.on_restart() for th in th_q]

    def close():
        """ close test case """
        global th_q
        [th.join(0.5) for th in th_q]
        post['PYDISPLAY'].on_close()


    @profile
    def test(cb_typ):
        ini(cb_typ)
        run()
        close()

    try:
        [test(cb_typ=cb) for cb in cbs.keys()]
    except PyError:
        raise "demo_callback error"


def demo_parallel_loop(n=100000):
    """ demo parallel via cython/python parallel or not """

    jobs = {
        'CYNOPARALLEL' : ccycheese.cysumpar_no_parallel(n),
        'CYONPARALLEL' : ccycheese.cysumpar_on_parallel(n),
        'PYNOPARALLEL' : ccycheese.pysumpar_no_parallel(n),
        'PYONPARALLEL' : ccycheese.pysumpar_on_parallel(n)
        }

    @profile
    def test(jb_typ):
        print "run %s " %(jb_typ)
        print "accumulate sum is %d" %(jobs[jb_typ])

    try:
        [test(jb_typ=jb) for jb in jobs.keys()]
    except PyError:
        raise "demo_parallel_loop error"


def demo_pipeline_loop(jb_typ='', rerun=3):
    """ demo pipeline loop via cython/python pipeline or not """

#    jobs = {
#        'CYNOPIPELINE' : ccycheese.cysumpar_no_pipeline(n),
#        'CYONPIPELINE' : ccycheese.cysumpar_on_pipeline(n),
#        'PYNOPIPELINE' : ccycheese.pysumpar_no_pipeline(n),
#        'PYONPIPELINE' : ccycheese.pysumpar_on_pipeline(n)
#        }
#
#    def test():
#        pass
#
#    try:
#        test()
#    except PyError:
#        raise "demo_pipeline_loop error"
#

@profile
def demo_pthread_no_gil():
    try:
        cpypthread.spawn_non_python_thread(pycallback.wap_on_pthread_callback)
    except PyError:
        raise "demo_pthread_no_gil"


def main():
    """ doctest """

#    demo_callback()
    demo_parallel_loop()
#    demo_pipeline_loop()

#    demo_pthread_no_gil()

if __name__ == '__main__':
    main()
