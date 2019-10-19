#include "vector.h"
#define ARRAY_CLEARED(name, type, size) \
    type name[size] = { 0 }; \
    memset(&name[0], 0, sizeof(name));

static char*
generate_vector(char* Type) {
    char* Name = calloc(100, sizeof(char));
    strcat(Name, "vector_");
    strcat(Name, Type);

    // Make sure that the Type of vector container
    // that is getting generated does not already exist.
    if (VecTypes.Type == NULL) {
        VecTypes.Type = calloc(strlen(Type), sizeof(char));
        strcpy(VecTypes.Type, Type);
    } else {
        if (not_in_list(&VecTypes, Type)) {
            add_type_to_list(&VecTypes, Type);
        } else {
            return Name;
        }
    }

    // Guard to protect against redefinition
    ADD_TO_VEC("#ifndef VECTOR_");
    ADD_TO_VEC(Type);
    ADD_TO_VEC("_\n");
    ADD_TO_VEC("#define VECTOR_");
    ADD_TO_VEC(Type);
    ADD_TO_VEC("_\n");

    // Generate the vec struct
    // Typedef struct {
    //     Type* Items;
    //     int TotSize;
    //     int CurSize;
    // } vector_Type;
    ADD_TO_VEC("typedef struct {\n");
    ADD_TO_VEC(TAB);
    ADD_TO_VEC(Type);
    ADD_TO_VEC("* Items;\n");
    ADD_TO_VEC(TAB);
    ADD_TO_VEC("int TotSize;\n");
    ADD_TO_VEC(TAB);
    ADD_TO_VEC("int CurSize;\n");
    ADD_TO_VEC("} ");
    ADD_TO_VEC(Name);
    ADD_TO_VEC(";\n");

    // Generate the function calls
    //
    //
    // void Vector_'Type'_init(Vector_'Type' *Vec) {
    //      Vec->Items = malloc(100 * sizeof('Type'));
    //      Vec->TotSize = 100;
    //      Vec->CurSize = 0;
    // }
    ADD_TO_VEC("void ");
    ADD_TO_VEC(Name);
    ADD_TO_VEC("_init(");
    ADD_TO_VEC(Name);
    ADD_TO_VEC(" *Vec) {\n");
    ADD_TO_VEC(TAB);
    ADD_TO_VEC("Vec->Items = malloc(100 * sizeof(");
    ADD_TO_VEC(Type);
    ADD_TO_VEC("));\n");
    ADD_TO_VEC(TAB);
    ADD_TO_VEC("Vec->TotSize = 100;\n");
    ADD_TO_VEC(TAB);
    ADD_TO_VEC("Vec->CurSize = 0;\n");
    ADD_TO_VEC("}\n");

    // void vector_'Type'_expand(vector_'Type' *Vec) {
    //     Vec->TotSize = Vec->TotSize  * 2;
    //     Vec->Items = realloc(Vec->Items, sizeof('Type') * Vec->TotSize);
    // }
    ADD_TO_VEC("void vector_");
    ADD_TO_VEC(Type);
    ADD_TO_VEC("_expand(vector_");
    ADD_TO_VEC(Type);
    ADD_TO_VEC(" *Vec) {\n");
    ADD_TO_VEC(TAB);
    ADD_TO_VEC("Vec->TotSize = Vec->TotSize * 2;\n");
    ADD_TO_VEC(TAB);
    ADD_TO_VEC("Vec->Items = realloc(Vec->Items, sizeof(");
    ADD_TO_VEC(Type);
    ADD_TO_VEC(") * Vec->TotSize);\n");
    ADD_TO_VEC("}\n");

    // void Vector_'Type'_push(Vector_'Type' *Vec, 'Type' Item) {
    //      if (Vec->TotSize == Vec->CurSize) {
    //      }
    //      Vec->Items[Vec->CurSize++] = Item;
    //  }
    ADD_TO_VEC("void ");
    ADD_TO_VEC(Name);
    ADD_TO_VEC("_push(");
    ADD_TO_VEC(Name);
    ADD_TO_VEC(" *Vec, ");
    ADD_TO_VEC(Type);
    ADD_TO_VEC(" Item) {\n");
    ADD_TO_VEC(TAB);
    ADD_TO_VEC("if (Vec->TotSize == Vec->CurSize) {\n");
    ADD_TO_VEC(TAB);
    ADD_TO_VEC(TAB);
    ADD_TO_VEC("vector_");
    ADD_TO_VEC(Type);
    ADD_TO_VEC("_expand(Vec);\n");
    ADD_TO_VEC(TAB);
    ADD_TO_VEC("}\n");
    ADD_TO_VEC(TAB);
    ADD_TO_VEC("Vec->Items[Vec->CurSize++] = Item;\n");
    ADD_TO_VEC("}\n");

    //void vector_'Type'_insert(vector_'Type' *Vec, 'Type' Pos, 'Type' Item) {
    //    for ('Type' i = Vec->CurSize + 1; i > Pos - 1; i--) {
    //        Vec->Items[i+1] = Vec->Items[i]; 
    //    }
    //    Vec->Items[Pos] = Item;
    //    Vec->CurSize++;
    //}
    ADD_TO_VEC("void vector_");
    ADD_TO_VEC(Type);
    ADD_TO_VEC("_insert(vector_");
    ADD_TO_VEC(Type);
    ADD_TO_VEC(" *Vec, int Pos, ");
    ADD_TO_VEC(Type);
    ADD_TO_VEC(" Item) {\n");
    ADD_TO_VEC(TAB);
    ADD_TO_VEC("if (Vec->TotSize == Vec->CurSize) {\n");
    ADD_TO_VEC(TAB);
    ADD_TO_VEC(TAB);
    ADD_TO_VEC("vector_");
    ADD_TO_VEC(Type);
    ADD_TO_VEC("_expand(Vec);\n");
    ADD_TO_VEC(TAB);
    ADD_TO_VEC("}\n");
    ADD_TO_VEC(TAB);
    ADD_TO_VEC("for (int i = Vec->CurSize + 1; i > Pos - 1; i--) {\n");
    ADD_TO_VEC(TAB);
    ADD_TO_VEC(TAB);
    ADD_TO_VEC("Vec->Items[i+1] = Vec->Items[i];\n");
    ADD_TO_VEC(TAB);
    ADD_TO_VEC("}\n");
    ADD_TO_VEC(TAB);
    ADD_TO_VEC("Vec->Items[Pos] = Item;\n");
    ADD_TO_VEC(TAB);
    ADD_TO_VEC("Vec->CurSize++;\n");
    ADD_TO_VEC("}\n");

    //  inline 'Type'* vector_'Type'_at(vector_'Type' Vec, int Pos) {
    //      return &Vec.Items[Pos]
    //  }
    ADD_TO_VEC("static inline ");
    ADD_TO_VEC(Type);
    ADD_TO_VEC("* vector_");
    ADD_TO_VEC(Type);
    ADD_TO_VEC("_at(vector_");
    ADD_TO_VEC(Type);
    ADD_TO_VEC(" Vec, int Pos) {\n");
    ADD_TO_VEC(TAB);
    ADD_TO_VEC("return &Vec.Items[Pos];\n");
    ADD_TO_VEC("}\n");

    // inline 'Type'* vector_'Type'_front(vector_'Type' Vec) {
    //      return &Vec.Items[0];
    // }
    ADD_TO_VEC("static inline ");
    ADD_TO_VEC(Type);
    ADD_TO_VEC("* vector_");
    ADD_TO_VEC(Type);
    ADD_TO_VEC("_front(vector_");
    ADD_TO_VEC(Type);
    ADD_TO_VEC(" Vec) {\n");
    ADD_TO_VEC(TAB);
    ADD_TO_VEC("return &Vec.Items[0];\n");
    ADD_TO_VEC("}\n");

    // static inline void vector_'Type'_free(vector_'Type' *Vec) {
    //      free(Vec->Items);
    //      Vec->Items = 0;
    //      Vec->CurSize = 0;
    //      Vec->TotSize = 0;
    // }
    ADD_TO_VEC("static inline void vector_");
    ADD_TO_VEC(Type);
    ADD_TO_VEC("_free(vector_");
    ADD_TO_VEC(Type);
    ADD_TO_VEC(" *Vec) {\n");
    ADD_TO_VEC(TAB);
    ADD_TO_VEC("free(Vec->Items);\n");
    ADD_TO_VEC(TAB);
    ADD_TO_VEC("Vec->Items = 0;\n");
    ADD_TO_VEC(TAB);
    ADD_TO_VEC("Vec->CurSize = 0;\n");
    ADD_TO_VEC(TAB);
    ADD_TO_VEC("Vec->TotSize = 0;\n");
    ADD_TO_VEC("}\n");

    // End the redefinition guard
    ADD_TO_VEC("#endif\n");

    return Name;
}

static bool
parse_vector_var(char* VarName) {
    get_next_token();
    if (CurTok == '[') {
        ADD_TO_NORMAL("*vector_");
        ADD_TO_NORMAL(get_var_type(&VecVariables, VarName));
        ADD_TO_NORMAL("_at(");
        ADD_TO_NORMAL(VarName);
        ADD_TO_NORMAL(", ");
        
        get_next_token();
		if (CurTok == tok_constant || CurTok == tok_identifier) {
		    ADD_TO_NORMAL(IdentifierStr);
		} else if (CurTok > 0) {
            NormalOutput[NormalIndex++] = (char) CurTok;
        } else {
        	return log_error("Expected number after '['", CurrentLine);
        }
        ADD_TO_NORMAL(")");
		
    } else {
        ARRAY_CLEARED(Error, char, 100);
        strcat(Error, "Unknown symbol after ");
        strcat(Error, VarName);
        strcat(Error, ".");
        return log_error(Error, CurrentLine);
    }
    get_next_token(); // eat ']'
    
    return true;
}

static bool
parse_vector_function() {
    get_next_token();

    if (strcmp(IdentifierStr, "push") == 0) {
        // vector_push(var, value);
        get_next_token(); // Eat 'push'

        get_next_token(); // Eat '('

        func_call_args Args = get_func_args();

        // Expect the first argument to be VarName
        char* VarName = Args.Arg;

        char* VarType = get_var_type(&VecVariables, VarName);
        if (!VarType) {
            return false;
        }

        ARRAY_CLEARED(FuncName, char, 100);
        strcat(FuncName, "vector_");
        strcat(FuncName, VarType);
        strcat(FuncName, "_push");

        ADD_TO_NORMAL(FuncName);
        ADD_TO_NORMAL("(&");
        ADD_TO_NORMAL(VarName);
        ADD_TO_NORMAL(", ");
        ADD_TO_NORMAL(Args.Next->Arg);

        output_remaining_func_line();
        free_func_call_args(Args);
    }
    if (strcmp(IdentifierStr, "at") == 0) {
        // vector_at(var, index);
        get_next_token(); // Eat 'at'
        
        get_next_token(); // Eat '('
        
        func_call_args Args = get_func_args();

        // Expect the first argument to be VarName
        char* VarName = Args.Arg;

        char* VarType = get_var_type(&VecVariables, VarName);
        ARRAY_CLEARED(FuncName, char, 100);
        strcat(FuncName, "*vector_");
        strcat(FuncName, VarType);
        strcat(FuncName, "_at");

        ADD_TO_NORMAL(FuncName);
        ADD_TO_NORMAL("(");
        ADD_TO_NORMAL(VarName);
        ADD_TO_NORMAL(", ");
        ADD_TO_NORMAL(Args.Next->Arg);

        output_remaining_func_line();
        free_func_call_args(Args);
    }
    if (strcmp(IdentifierStr, "front") == 0) {
        // vector_front(var)
        get_next_token(); // Eat 'front'
        get_next_token(); // Eat '('

        func_call_args Args = get_func_args();

        // Expect the first argument to be VarName
        char* VarName = Args.Arg;

        char* VarType = get_var_type(&VecVariables, VarName);
        ARRAY_CLEARED(FuncName, char, 100);
        strcat(FuncName, "*vector_");
        strcat(FuncName, VarType);
        strcat(FuncName, "_front");

        ADD_TO_NORMAL(FuncName);
        ADD_TO_NORMAL("(");
        ADD_TO_NORMAL(VarName);

        output_remaining_func_line();
        free_func_call_args(Args);
    }

    if (strcmp(IdentifierStr, "insert") == 0) {
        // vector_insert(var, pos, item)
        get_next_token(); // Eat 'insert'
        get_next_token(); // Eat '('

        func_call_args Args = get_func_args();

        // Expect the first argument to be VarName
        char* VarName = Args.Arg;

        char* VarType = get_var_type(&VecVariables, VarName);
        ARRAY_CLEARED(FuncName, char, 100);
        strcat(FuncName, "vector_");
        strcat(FuncName, VarType);
        strcat(FuncName, "_insert(&");

        ADD_TO_NORMAL(FuncName);

        func_call_args* Iterator = &Args;
        while (Iterator->Next != NULL) {
            ADD_TO_NORMAL(Iterator->Arg); 
            ADD_TO_NORMAL(", ");

            Iterator = Iterator->Next;
        }
        ADD_TO_NORMAL(Iterator->Arg);

        output_remaining_func_line();
        free_func_call_args(Args);
    }

    if (strcmp(IdentifierStr, "free") == 0) {
        // vector_free(var)
        get_next_token(); // Eat 'free'
        get_next_token(); // Eat '('

        func_call_args Args = get_func_args();

        // Expect the first argument to be VarName
        char* VarName = Args.Arg;

        char* VarType = get_var_type(&VecVariables, VarName);
        ARRAY_CLEARED(FuncName, char, 100);
        strcat(FuncName, "vector_");
        strcat(FuncName, VarType);
        strcat(FuncName, "_free");

        ADD_TO_NORMAL(FuncName);
        ADD_TO_NORMAL("(&");
        ADD_TO_NORMAL(VarName);

        output_remaining_func_line();
        free_func_call_args(Args);
    }
    return true;
}

// Caller Requirements: free returned value
static char*
get_vector_file_name() {
    char* VecOutName = (char *)calloc(100, sizeof(char));
    strcat(VecOutName, "__vector");
    ARRAY_CLEARED(Num, char, 10);
    sprintf(Num,"%d",SourceFileCount);
    strcat(VecOutName, Num);
    strcat(VecOutName, ".h");
    return VecOutName;
}

static bool
parse_vector() {
	if (CurVecFile < SourceFileCount) {
        ARRAY_CLEARED(IncludeStr, char, 100);

        strcat(IncludeStr, "#include \"");
        char* FileName = get_vector_file_name();
        strcat(IncludeStr, FileName);
        free(FileName);
        strcat(IncludeStr, "\"\n");
		CurVecFile++;
		ADD_TO_GLOBAL(IncludeStr);

        // Need this for malloc and realloc
        ADD_TO_VEC("#include <stdlib.h>\n");
	}
	

	// Parse argument inside of '< >'
    get_next_token(); // Eat 'vector'

    if (CurTok == '_')
        return parse_vector_function();

    if (CurTok != '<')
        return log_error("Expected '<' in vector declaration", CurrentLine);
    get_next_token(); // Eat '<'

    char Type[100] = { 0 };
    strcpy(Type, IdentifierStr);
    char* VecName = generate_vector(Type);

    get_next_token();
    if (CurTok != '>')
        return log_error("Expected '>' in vector declaration", CurrentLine);

    char VarName[100] = { 0 };

    // Look for the var name
    while (CurTok != tok_identifier) {
        // If you hit the semicolon before finding a var name
        if (CurTok == ';') {
            return log_error("Expected variable name in vector declaration", CurrentLine);
        }

        get_next_token();
    }
    while (CurTok != ';') {
        if (CurTok == tok_identifier) {
            strcat(VarName, IdentifierStr);
        } else {
            int Len = strlen(VarName);
            VarName[Len] = CurTok;
        }
        get_next_token();
    }
    get_next_token(); // eat the newline


    if (VecVariables.Name == NULL) {
        VecVariables.Name = calloc(strlen(VarName), sizeof(char));
        strcpy(VecVariables.Name, VarName);

        VecVariables.Type = calloc(strlen(Type), sizeof(char));
        strcpy(VecVariables.Type, Type);
    } else {
        add_var_to_list(&VecVariables, Type, VarName);
    }

    // Change the variable name declaration
    // vector_'Type' name;
    ADD_TO_NORMAL(VecName);
    ADD_TO_NORMAL(" ");
    free(VecName);
    ADD_TO_NORMAL(VarName);
    ADD_TO_NORMAL(";\n");

    // Insert a call to vector_'Type'_init
    add_tabs_to_normal_output();
    ADD_TO_NORMAL("vector_");
    ADD_TO_NORMAL(Type);
    ADD_TO_NORMAL("_init(&");
    ADD_TO_NORMAL(VarName);
    ADD_TO_NORMAL(");\n");

    return true;
}

static void
empty_vec_types() {
    empty_type_list(&VecTypes);
}
