#include <stdlib.h>
#include <stdio.h>
#include "test2.h"

typedef struct {
    int a;
    int b;
    int c;
} Integers;
int main() {
    vector<Integers> this_var;
    Integers a = {1,2,3};
    vector_push(this_var, a);
    vector_front(this_var);

    vector<int> test;
    vector<char> test2;
    if (1) {
        vector<double> test3;
        vector_free(test3);

        if (1) {
            vector<double> test4;
            vector_free(test4);
        }
    }
    for (int i = 0; i < 300; i++) {
        vector_insert(test, 0, i);
    }
    for (int i = 0; i < 300; i++) {
        printf("%d\n", vector_at(test, i));
    }
    vector_push(test2, 10);

    vector_free(this_var);
    vector_free(test);
    vector_free(test2);
}
