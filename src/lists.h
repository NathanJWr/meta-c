#ifndef LISTS_H_
#define LISTS_H_
typedef struct _variables {
    char* Name;
    char* Type;

    struct _variables *Next;
} variables;

typedef struct _types {
    char* Type;

    struct _types *Next;
} types;

static void empty_type_list(types *Types);
static void add_type_to_list(types *Types, char *TypeName);
static void add_var_to_list(variables *Vars, char *TypeName, char* VarName);
static bool not_in_list(types *Types, char *TypeName);
static char* get_var_type(variables *Vars, char* VarName);

#endif

