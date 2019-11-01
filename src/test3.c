#include <stdio.h>
int print_vec(vector<int> vec) {
    for (int i = 0; i < 1000; i++) {
        printf("%d ", test[i]);
    }
}
int main() {
    vector<int> test;
    for (int i = 0; i < 1000; i++) {
        vector_push(test, i);
    }
    print_vec(test)
}
