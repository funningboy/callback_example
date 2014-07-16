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

int end = 0;

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
//  PyObject *mod, *func, *rst;
//  mod PyEval_ini
//  func =
//  rst =
//  Py_Initialize();
//  mod = PyImport_ImportModule("run_cheese");
//  assert(mod!=NULL && "import run_cheese error");
//  PyObject *c_api_object = PyObject_GetAttrString(module, "_C_API");
//  arglist = Py_BuildValue("(i)", arg);
//  result = PyEval_CallObject(my_callback, arglist);
//  Py_BuildValue("i", );
//
//  while (!end) {
//    char** p = cheeses;
//    while (*p) {
//
//      ++p;
//    }
//  }
//
}
