
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <errno.h>
#include <Python.h>

#define PY_MAJOR_VERSION 2
static PyObject* spawn_non_python_thread(PyObject *self, PyObject *args);
static PyThreadState *threadState;
static PyObject *error;
