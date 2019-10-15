typedef struct _variables {
    char* Name;
    char* Type;

    struct _variables *Next;
} variables;

typedef struct _types {
    char* Type;

    struct _types *Next;
} types;


static void empty_type_list(types *Types) {
    types *Iterator = Types;

    // Free the first one manually because the head is
    // allocated on the stack and doesn't have to be 
    // freed like the rest of the nodes
    free(Iterator->Type);
    Iterator = Iterator->Next;
    while (Iterator) {
        free(Iterator->Type);
        types* Tmp = Iterator;
        Iterator = Iterator->Next;
        free(Tmp);
    }
    Types->Next = NULL;
    Types->Type = NULL;
}
static void add_type_to_list(types *Types, char *TypeName) {
    types *NewNode = malloc(sizeof(types));
    NewNode->Type = (char *) malloc(strlen(TypeName) * sizeof(char));
    NewNode->Next = NULL;

    strcpy(NewNode->Type, TypeName);

    types *LastNode = Types;

    while (LastNode->Next != NULL) {
        LastNode = LastNode->Next;
    }

    LastNode->Next = NewNode;
}

static void add_var_to_list(variables *Vars,
                            char *TypeName,
                            char* VarName) {
    variables *NewNode = malloc(sizeof(variables));
    NewNode->Name = (char *) malloc(strlen(VarName) * sizeof(char));
    NewNode->Type = (char *) malloc(strlen(TypeName) * sizeof(char));
    NewNode->Next = NULL;

    strcpy(NewNode->Type, TypeName);
    strcpy(NewNode->Name, VarName);

    variables *LastNode = Vars;

    while (LastNode->Next != NULL) {
        LastNode = LastNode->Next;
    }

    LastNode->Next = NewNode;
}

static bool not_in_list(types *Types, char *TypeName) {
    types *Iterator = Types;
    while (Iterator != NULL) {
        if (strcmp(Iterator->Type, TypeName) == 0)
            return false;

        Iterator = Iterator->Next;
    }
    return true;
}

static char* get_var_type(variables *Vars, char* VarName) {
    variables *Iterator = Vars;
    while (Iterator != NULL) {
        if (strcmp(Iterator->Name, VarName) == 0) {
            return Iterator->Type;
        }
        Iterator = Iterator->Next;
    }
    // There is no variable VarName in the list
    char Error[100] = "No type found associated with ";
    strcat(Error, VarName);
    log_error(Error, CurrentLine);
    return NULL;
}
