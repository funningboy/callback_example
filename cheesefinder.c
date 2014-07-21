/*
 *   An example of a C API that provides a callback mechanism.
 */

#include "cheesefinder.h"
static char *cheeses[] = {
  "cheddar",
  "camembert",
  "that runny one",
  0
};

static PyThreadState *threadState;

/* callback as void* */
void find_cheeses(cheesefunc user_func, void *user_data) {
   while (!end) {
        char **p = cheeses;
        while (*p) {
          user_func(*p, user_data);
          ++p;
        }
  }
}

/* callback as python callfunc */
void find_cheeses_py() {
  PyObject *mod, *func, *val;
  void* rst;

  PySys_SetPath(".");

  // impoty run_cheese module
  mod = PyImport_ImportModule("run_cheese");
  assert(mod != NULL && "import run_cheese error");

  // Release the global interpreter lock
  threadState = PyEval_SaveThread();

  while (!end) {
    char** p = cheeses;

    while (*p) {

      // Acquire the global interpreter lock
      PyEval_RestoreThread(threadState);

      func = PyObject_GetAttrString(mod, "wap_on_callback_py");
      assert(func != NULL && "run_cheese.wap_on_callback_py error");

      val = Py_BuildValue("(s)", *p);
      rst = PyEval_CallObject(func, val);
      assert(rst != NULL && "run_cheese.wap_on_callback_py error");

      Py_XINCREF(mod);
      Py_XINCREF(func);

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
}
