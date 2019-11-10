#include <stdio.h>
void pass_list(list<int> nums) {
    // test access to first item
    int i;
    printf("Numbers passed in: ");
    for (i = 0; i < nums.length; i++) {
        printf("%d ", nums[i])
    }
}

int main() {
    list<int> nums;
    list_init(nums);
    for (int i = 0; i < 10; i++) {
        list_pushfront(nums, i);
    }
    for (int i = 0; i < 10; i++) {
        list_pushback(nums, i);
    }
    for (int i = 0; i < 20; i++) {
        printf("%d\n", list_at(nums, i));
    }
    for (int i = 0; i < 20; i++) {
        printf("%d\n", nums[i]);
    }
    pass_list(nums);

    list<char> chars;
    list_init(chars);
    for (int i = 0; i < 26; i++) {
        list_pushback(chars, 'a' + i);
    }
    for (int i = 0; i < 26; i++) {
        printf("%c\n", list_front(chars));
        list_popfront(chars);
    }

    list_free(nums);
}
