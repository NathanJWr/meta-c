#include <stdio.h>
#include <assert.h>
typedef struct {
    int num1;
    int num2;
} LargeNumber;
void test_all_functions_with_pointer() {
    vector<int>* nums = malloc(sizeof(vector<int>));
    vector_init(nums);

    int i;
    for (i = 0; i < 1000; i++) {
        vector_pushback(nums, i);
    }
    for (i = 0; i < 1000; i++) {
        assert(nums[i] == i);
    }
    nums[50] = 4812;
    assert(vector_at(nums, 50) == 4812);


    vector_free(nums);
}
void test_all_function_calls() {
    int i;
    vector<char> chars;
    vector_init(chars);

    for (i = 0; i < 10; i++) {
        vector_pushback(chars, 'a' + i);
    }
    for (i = 0; i < 10; i++) {
        assert(chars[i] == 'a' + i);
    }
    chars[5] = 'z';
    assert(vector_at(chars, 5) == 'z');

    vector_insert(chars, 10, 'z');
    assert(chars[10] == 'z');
}
int main() {
    test_all_function_calls();
}