/*
 *   An example of a C API that provides a callback mechanism.
 */

#include "ccycheesefinder.h"
static char *cheeses[] = {
  "cheddar",
  "camembert",
  "that runny one",
  0
};

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

/* dynamic list */
int* dynamic_list(int n) {
  int *a = (int*) malloc(n * sizeof(int));
  for(int i = 0; i<n; i++) {
    a[i] = i;
  }
  return a;
}
