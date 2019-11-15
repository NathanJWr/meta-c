#include <stdio.h>
#include <assert.h>
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