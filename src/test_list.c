#include <stdio.h>
void free_half(list<char>* chars) {
    int i;
    for (i = 0; i < chars->length / 2; i++) {
        list_popfront(chars);
    }
}

void pass_list(list<int> nums) {
    int i;
    printf("Numbers passed in using '[]': ");
    for (i = 0; i < nums.length; i++) {
        printf("%d ", nums[i]);
    }
    printf("\n");
    printf("Numbers passed in using list_at: ");
    for (i = 0; i < nums.length; i++) {
        printf("%d ", list_at(nums, i));
    }
    printf("\n");
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
    pass_list(nums);

    list<char> chars;
    list_init(chars);
    for (int i = 0; i < 26; i++) {
        list_pushback(chars, 'a' + i);
    }
    printf("chars length before free_half: %d\n", chars.length);
    free_half(&chars);
    printf("chars length after free_half: %d\n", chars.length);
    for (int i = 0; i < 26; i++) {
        printf("%c\n", list_front(chars));
        list_popfront(chars);
    }
    list_free(nums);
    list_free(chars);
}
