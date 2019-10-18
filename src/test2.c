#include <stdlib.h>
#include "test2.h"
#include <stdio.h>
int main() {
    vector<int> test;
    for (int i = 0; i < 10; i++) {
        vector_insert(test, 0, i);
    }
    for (int i = 0; i < 10; i++) {
        printf("%d", vector_at(test, i));
    }
    vector_free(test);
}
