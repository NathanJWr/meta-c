#include <stdio.h>
int main() {
    int i;
    vector<int> nums;
    vector_init(nums);
    for (i = 0; i < 100; i++) {
        vector_push(nums, i);
    }
}