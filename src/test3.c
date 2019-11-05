#include <stdio.h>
typedef struct {
    int a;
} something;
something*** print_vec(vector<int> vec) {
    for (int i = 0; i < 1000; i++) {
        printf("%d ", vec[i]);
    }
}
int main() {
    vector<int> test;
    vector_init(test);
    for (int i = 0; i < 1000; i++) {
        vector_push(test, i);
    }
    print_vec(test);
}
