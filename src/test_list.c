#include <stdio.h>
int main() {
    list<int> nums;
    list_init(nums);
    for (int i = 0; i < 100; i++) {
        list_push(nums, i);
    }
    for (int i = 0; i < 100; i++) {
        printf("%d\n", list_front(nums));
        list_pop(nums);
    }
}
