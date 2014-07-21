
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <Python.h>

typedef void (*cheesefunc)(char *name, void *user_data);
void find_cheeses(cheesefunc user_func, void *user_data);
void find_cheeses_py();
static int end = 0;
