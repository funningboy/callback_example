#
#   Cython wrapper for the cheesefinder API
#
cdef extern from "cycheesefinder.h":
    ctypedef void (*cheesefunc)(char *name, void *user_data)
    void find_cheeses(cheesefunc user_func, void *user_data) nogil
    int end
    int* dynamic_list(int n)

cimport cython
from cython.parallel import prange
import numpy as np
import subprocess
import multiprocessing

#---------------------
# demo callback block
#---------------------
def find(f):
    with nogil:
        find_cheeses(callback, <void*>f)

cdef void callback(char *name, void *f) nogil:
    with gil:
        (<object>f)(name)

def on_stop():
    global end
    end = 1

def on_restart():
    global end
    end = 0

#----------------------
# demo parallel loop block
#----------------------
@cython.nonecheck(False)
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(False)
@cython.profile(True)
cpdef cysumpar_no_parallel(int n):
    """ as cython parallel loop off """
    cdef int tot=0
    cdef int* a = dynamic_list(n)
    for i in range(n):
        tot += a[i]
    return tot

@cython.nonecheck(False)
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(False)
@cython.profile(True)
cpdef cysumpar_on_parallel(int n):
    """ as cython parallel loop on """
    cdef int tot=0
    cdef int* a = dynamic_list(n)
    cdef int i
    for i in prange(n, nogil=True):
        tot += a[i]
    return tot


def pysumpar_no_parallel(n):
    """ as python parallel loop off """
    tot = 0
    cdef int* a = dynamic_list(int(n))
    for i in range(int(n)):
        tot += a[i]
    return tot


def pysumpar_on_parallel(n):
    """ as python parallel loop on """
    pass

#----------------------
# demo hyper c/py with nump
#----------------------
def gibbs(int N=20000,int thin=500):
    cdef double x=0
    cdef double y=0
    cdef int i, j
    samples = []
    for i in range(N):
        for j in range(thin):
            x=np.random.gamma(3,1.0/(y*y+4))
            y=np.random.normal(1.0/(x+1),1.0/np.sqrt(x+1))
        samples.append((x,y))
    return samples

#----------------------
# demo pthread no python GIL
#----------------------

