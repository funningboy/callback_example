
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <Python.h>

#define PY_MAJOR_VERSION 2
static PyObject* find_cheeses(PyObject *self, PyObject *args);
static int end = 0;
static PyThreadState *threadState;
static PyObject *error;


