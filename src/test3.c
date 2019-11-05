#include <stdio.h>
#include "__test4.h"
int main() {
    vector<int> test;
    vector_init(test);
    for (int i = 0; i < 1000; i++) {
        vector_push(test, i);
    }
    print_vec(test);
}
