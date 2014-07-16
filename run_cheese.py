import cheese
import threading

async = []

class PyCheese(threading.Thread):
    """ as Python GIL for C callback """

    def __init__(self):
        super(PyCheese, self).__init__()
        self._count = 0
        #self._typs  = {
        #        'NORMALCB' : cheese.find(self.on_callback),
        #        'PYTOHNCB' : cheese.find_py()
        #        }
        #self._typ = 'NORMALCB'

    def run(self):
        """ register callback(report_cheese) to c """
        #self._typs[self._typ]
        cheese.find(self.on_callback)

    def on_callback(self, name):
        global async
        async.append(name)
        self._count += 1

    def on_callback_py(self, name):
        global async
        async.append(name)
        self._count += 1

    def on_stop(self):
        cheese.on_stop()

    def on_restart(self):
        pass


class PyDisplay(threading.Thread):
    """ as Python GIL for py proc """

    def __init__(self):
        super(PyDisplay, self).__init__()

    def run(self):
        """  """
        global async
        while (async):
            print "%s" %(async.pop())

    def on_stop(self):
        pass

    def on_restart(self):
        pass

th_0 = PyCheese()
th_1 = PyDisplay()
th_0.setDaemon(True)
th_1.setDaemon(True)
th_0.start()
th_1.start()
while th_0._count < 3:
    pass
th_0.on_stop()
th_1.on_stop()
th_0.join()
th_1.join()
