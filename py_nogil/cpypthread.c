/*
 * An example of a C pthread whithout python gil
 */

#ifdef __cplusplus
extern "C" {
#endif

#include "cpypthread.h"

static void*
non_python_thread(void *python_callback) {

  PyGILState_STATE state = PyGILState_Ensure();

  PyObject* stdout = PySys_GetObject("stdout");
  if (stdout == NULL) {
    PyErr_SetString(PyExc_RuntimeError,  "no stdout");
    goto done;
  }
  Py_INCREF(stdout);
  if (PyFile_WriteString("non-python thread\n", stdout) != 0) {
    Py_DECREF(stdout);
    goto done;
  }
  else {
#if PY_MAJOR_VERSION < 3
      PyFile_SoftSpace(stdout, 0); // softspace = False after a newline
#endif
    Py_DECREF(stdout);
  }

  PyObject* ignored = PyObject_CallFunctionObjArgs(python_callback, NULL);
  Py_XDECREF(ignored);

done:
  PyGILState_Release(state);
  return NULL;
}


static PyObject *
spawn_non_python_thread(PyObject *self, PyObject *args) {

  PyObject* ret = NULL;
  // register callback to thread target
  PyObject* python_callback = NULL;
  if (!PyArg_ParseTuple(args, "O:spawn_non_python_thread", &python_callback))
    return NULL;
  Py_INCREF(python_callback); // hold on to it until the thread is finished

  Py_BEGIN_ALLOW_THREADS
  // eq as { PyThreadState *_save; _save = PyEval_SaveThread(); }

  pthread_t tid;
  int s = 0;
  if ((s = pthread_create(&tid, NULL, non_python_thread, python_callback))!= 0) {
    errno = s;
    Py_BLOCK_THREADS
    // eq as PyEval_RestoreThread(_save);
    PyErr_SetFromErrno(PyExc_OSError); goto done;
  }
  else if ((s = pthread_join(tid, NULL)) != 0) {
    errno = s;
    Py_BLOCK_THREADS
    PyErr_SetFromErrno(PyExc_OSError); goto done;
  }
  else {
    Py_BLOCK_THREADS
    if (PyErr_Occurred() == NULL) {
      ret = Py_None; Py_INCREF(ret);
    }
  }

 done:
  Py_UNBLOCK_THREADS
  Py_END_ALLOW_THREADS
  Py_DECREF(python_callback);
  return ret;
}


static PyMethodDef moduleMethods[] = {
  {"spawn_non_python_thread", spawn_non_python_thread, METH_VARARGS, "spawn non python thread without gil"},
  {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef module = {
  PyModuleDef_HEAD_INIT,
  "cpypthread",     /* name of module */
  NULL,           /* module documentation, may be NULL */
  -1,             /* size of per-interpreter state of the module,
                  or -1 if the module keeps state in global variables. */
  moduleMethods
};
#endif

PyMODINIT_FUNC
#if PY_MAJOR_VERSION >= 3
PyInit_cpypthread(void)
#else
initcpypthread(void)
#endif
{
  PyObject *m, *mod;

#if PY_MAJOR_VERSION >= 3
  m = PyModule_Create(&module);
#else
  m = Py_InitModule("cpypthread", moduleMethods);
#endif

  if (m == NULL) {
#if PY_MAJOR_VERSION >= 3
    return NULL;
#endif
  }

  error = PyErr_NewException("cpypthread.error", NULL, NULL);
  Py_INCREF(error);
  PyModule_AddObject(m, "error", error);

  mod = PyImport_ImportModule("threading");
  Py_XDECREF(mod);

  PyEval_InitThreads();

#if PY_MAJOR_VERSION >=3
  return m;
#endif
}

#ifdef __cplusplus
}  // extern "C"
#endif
