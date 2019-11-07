#include <stdio.h>
int main() {
    list<int> nums;
    list_init(nums);
    for (int i = 0; i < 100; i++) {
        list_pushfront(nums, i);
    }
    for (int i = 0; i < 100; i++) {
        printf("%d\n", list_front(nums));
        list_popfront(nums);
    }

    list<char> chars;
    list_init(chars);
    for (int i = 0; i < 26; i++) {
        list_pushback(chars, 'a' + i);
    }
    for (int i = 0; i < 26; i++) {
        printf("%c\n", list_front(chars));
        list_popfront(chars);
    }
}
