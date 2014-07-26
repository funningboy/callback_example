
#include <stdio.h>
#include <stdlib.h>

typedef void (*cheesefunc)(char *name, void *user_data);
void find_cheeses(cheesefunc user_func, void *user_data);
static int end = 0;
int* dynamic_list(int n);
