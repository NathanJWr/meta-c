#include <stdio.h>
int main() {
    vector<int> test;
    for (int i = 0; i < 1000; i++) {
        vector_push(test, i);
    }
    for (int i = 0; i < 1000; i++) {
        printf("%d ", test[i]);
    }
}
