#include "output.h"
static void
add_to_output(char *Output, int *Index, char *Str) {
    int Size = strlen(Str);
    for (int i = 0; i < Size; i++) {
        Output[(*Index)++] = Str[i];
    }
}

static void
add_tabs_to_normal_output() {
    for (int i = 0; i < NumTabs; i++) {
        ADD_TO_NORMAL(TAB);
    }
}

static bool
log_error(const char *Str, int CurLine) {
    fprintf(stderr, "Error:%d: %s\n", CurLine + 1, Str);
    return false;
}
