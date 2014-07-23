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

#---------------------
# callback block
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
# parallel loop block
#----------------------
@cython.nonecheck(False)
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(False)
@cython.profile(True)
cpdef cysumpar_no_parallel(int n):
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
    """ as cython parallel loop """
    cdef int tot=0
    cdef int* a = dynamic_list(n)
    cdef int i
    for i in prange(n, nogil=True):
        tot += a[i]
    return tot

#----------------------
# pthread no python GIL
#----------------------
cdef
