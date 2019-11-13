#include <stdio.h>
#include <assert.h>
void change_list_ptr(list<char>** chars) {
    list<char>* new_chars = malloc(sizeof(list<char>));
    list_init(new_chars);
    list_pushback(new_chars, 'a');
    list_pushback(new_chars, 'b');
    list_pushback(new_chars, 'c');

    list_free(chars);
    free(*chars);

    *chars = new_chars;
}

void test_mallocing_list() {
    list<char>* chars = malloc(sizeof(list<char>));
    int i;

    list_init(chars);
    list_pushfront(chars, 'a');
    list_pushfront(chars, 'b');
    list_pushfront(chars, 'c');

    change_list_ptr(&chars);
    for (i = 0; i < chars->length; i++) {
        assert(chars[i] == 'a' + i);
        assert(list_at(chars, i) == 'a' + i);
    }

    list_free(chars);
    free(chars);
}

void test_all_functions_with_double_pointer(list<int>** nums) {
    list_init(nums);

    list_pushfront(nums, 1);
    list_pushback(nums, 2);
    assert(list_front(nums) == 1);
    list_popfront(nums);
    assert(list_front(nums) == 2);
    list_popfront(nums);
    list_pushback(nums, 3);
    assert(list_front(nums) == 3);
    list_pushfront(nums, 4);
    assert(nums[1] == 3);
    assert(list_at(nums, 1) == 3);
    list_free(nums);

}
void test_all_functions_with_pointer() {
    list<int>* nums = malloc(sizeof(list<int>));
    list_init(nums);

    list_pushfront(nums, 1);
    list_pushback(nums, 2);
    assert(list_front(nums) == 1);
    list_popfront(nums);
    assert(list_front(nums) == 2);
    list_popfront(nums);
    list_pushback(nums, 3);
    assert(list_front(nums) == 3);
    list_pushfront(nums, 4);
    assert(nums[1] == 3);
    assert(list_at(nums, 1) == 3);
    list_free(nums);

    test_all_functions_with_double_pointer(&nums);
    free(nums);
}
void test_all_functions() {
    list<int> nums;
    list_init(nums);

    list_pushfront(nums, 1);
    list_pushback(nums, 2);
    assert(list_front(nums) == 1);
    list_popfront(nums);
    assert(list_front(nums) == 2);
    list_popfront(nums);
    list_pushback(nums, 3);
    assert(list_front(nums) == 3);
    list_pushfront(nums, 4);
    assert(nums[1] == 3);
    assert(list_at(nums, 1) == 3);
    list_free(nums);
}

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
    test_mallocing_list();
    test_all_functions_with_pointer();

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
    printf("chars length before free_half: %zu\n", chars.length);
    free_half(&chars);
    printf("chars length after free_half: %zu\n", chars.length);
    for (int i = 0; i < 26; i++) {
        printf("%c\n", list_front(chars));
        list_popfront(chars);
    }
    list_free(nums);
    list_free(chars);
}
