""" profile """

import timeit
import logging
from guppy import hpy
import re
import json

reSIZE = re.compile(r"Total size = (\d+) bytes", re.M)

logging.basicConfig(filename='profile.log',level=logging.DEBUG)

def profile(func): #decorator **kwargs
    """ profile running time and logging it """

    def wrapper(*args, **kwargs): # func *args, **kwargs
        """ profile run time """
        t = timeit.Timer()
        retval = func(*args, **kwargs)
        hp = hpy()
        found = reSIZE.findall(str(hp.heap()))
        logging.info("call func %s",    func.__name__)
        logging.info("  arg %s",        json.dumps((args, kwargs)))
        logging.info("  run time %f s",     t.timeit())
        logging.info("  run mem %d bytes",  int(found[0]))
    return wrapper


