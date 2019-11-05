#include "__test4.h"
#include <stdio.h>
void print_vec(vector<int> vec) {
    for (int i = 0; i < 1000; i++) {
        printf("%d ", vec[i]);
    }
    return;
}
