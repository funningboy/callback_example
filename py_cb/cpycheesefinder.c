/*
 *   An example of a C API that provides a callback mechanism.
 */

#ifdef __cplusplus
extern "C" {
#endif

#include "cpycheesefinder.h"
static char *cheeses[] = {
  "cheddar",
  "camembert",
  "that runny one",
  0
};


/* as python c api func callback */
static PyObject*
find_cheeses(PyObject *self, PyObject *args)
{
  PyObject *mod, *func, *val;
  void* rst;

  // impoty run_cheese module
  mod = PyImport_ImportModule("pycallback");
  assert(mod != NULL && "import pycallback error");

  // Release the global interpreter lock
  threadState = PyEval_SaveThread();

  while (!end) {
    char** p = cheeses;

    while (*p) {

      // Acquire the global interpreter lock
      PyEval_RestoreThread(threadState);

      func = PyObject_GetAttrString(mod, "wap_on_callback"); //PyError
      assert(func != NULL && "pycallback.wap_on_callback error");

      val = Py_BuildValue("(s)", *p);
      rst = PyEval_CallObject(func, val);
      assert(rst != NULL && "pycallback.wap_on_callback error");

      Py_XINCREF(mod);
      Py_XINCREF(func);
      Py_XINCREF(val);
      ++p;

      // Release the global interpreter lock
      threadState = PyEval_SaveThread();
    }
  }

  Py_XDECREF(mod);
  Py_XDECREF(func);
  Py_XDECREF(val);

  // Release the global interpreter lock
  PyEval_RestoreThread(threadState);

  Py_INCREF(Py_None);
  return Py_None;
}


/* as python c api func callback */
static PyObject*
on_stop(PyObject *self, PyObject *args)
{
  end = 0;
  Py_INCREF(Py_None);
  return Py_None;
}


/* as python c api func callback */
static PyObject*
on_restart(PyObject *self, PyObject *args)
{
  end = 1;
  Py_INCREF(Py_None);
  return Py_None;
}


static PyMethodDef moduleMethods[] = {
  {"find",          find_cheeses, METH_NOARGS, "find_cheeses via python c api callback"},
  {"on_stop",       on_stop,      METH_NOARGS, "on_stop via python c api callback"},
  {"on_restart",    on_restart,   METH_NOARGS, "on_restart via python c api callback"},
  {NULL, NULL, 0, NULL}        /* Sentinel */
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef module = {
  PyModuleDef_HEAD_INIT,
  "c_pycheese",     /* name of module */
  NULL,           /* module documentation, may be NULL */
  -1,             /* size of per-interpreter state of the module,
                  or -1 if the module keeps state in global variables. */
  moduleMethods
};
#endif

PyMODINIT_FUNC
#if PY_MAJOR_VERSION >= 3
PyInit_cpycheese(void)
#else
initcpycheese(void)
#endif
{
  PyObject *m;

#if PY_MAJOR_VERSION >= 3
  m = PyModule_Create(&module);
#else
  m = Py_InitModule("cpycheese", moduleMethods);
#endif

  if (m == NULL) {
#if PY_MAJOR_VERSION >= 3
    return NULL;
#endif
  }

  error = PyErr_NewException("cpycheese.error", NULL, NULL);
  Py_INCREF(error);
  PyModule_AddObject(m, "error", error);

  PyEval_InitThreads();

#if PY_MAJOR_VERSION >=3
  return m;
#endif
}

#ifdef __cplusplus
}  // extern "C"
#endif
