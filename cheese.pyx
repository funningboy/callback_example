#
#   Cython wrapper for the cheesefinder API
#
cdef extern from "cheesefinder.h":
    ctypedef void (*cheesefunc)(char *name, void *user_data)
    void find_cheeses(cheesefunc user_func, void *user_data) nogil
#    void find_cheeses_py() nogil
    int end

def find(f):
    with nogil:
        find_cheeses(callback, <void*>f)

cdef void callback(char *name, void *f) nogil:
    with gil:
        (<object>f)(name)

#def find_py(f):
#    with nogil:
#        find_cheeses_py()

def on_stop():
    global end
    end = 1
