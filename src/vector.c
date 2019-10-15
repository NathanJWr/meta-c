static types VecTypes = { 0 };
static variables VecVariables = { 0 };

static char* generate_vector(char* Type) {
    char* Name = malloc(100 * sizeof(char));
    strcat(Name, "vector_");
    strcat(Name, Type);

    // Make sure that the Type of vector container
    // that is getting generated does not already exist.
    if (VecTypes.Type == NULL) {
        VecTypes.Type = malloc(strlen(Type) * sizeof(char));
        strcpy(VecTypes.Type, Type);
    } else {
        if (not_in_list(&VecTypes, Type)) {
            add_type_to_list(&VecTypes, Type);
        } else {
            return Name;
        }
    }

    // Guard to protect against redefinition
    add_to_output(VectorOutput, &VectorIndex, "#ifndef VECTOR_");
    add_to_output(VectorOutput, &VectorIndex, Type);
    add_to_output(VectorOutput, &VectorIndex, "_\n");
    add_to_output(VectorOutput, &VectorIndex, "#define VECTOR_");
    add_to_output(VectorOutput, &VectorIndex, Type);
    add_to_output(VectorOutput, &VectorIndex, "_\n");

    // Generate the vec struct
    // Typedef struct {
    //     Type* Items;
    //     int TotSize;
    //     int CurSize;
    // } vector_Type;
    add_to_output(VectorOutput, &VectorIndex, "typedef struct {\n");
    add_to_output(VectorOutput, &VectorIndex, TAB);
    add_to_output(VectorOutput, &VectorIndex, Type);
    add_to_output(VectorOutput, &VectorIndex, "* Items;\n");
    add_to_output(VectorOutput, &VectorIndex, TAB);
    add_to_output(VectorOutput, &VectorIndex, "int TotSize;\n");
    add_to_output(VectorOutput, &VectorIndex, TAB);
    add_to_output(VectorOutput, &VectorIndex, "int CurSize;\n");
    add_to_output(VectorOutput, &VectorIndex, "} ");
    add_to_output(VectorOutput, &VectorIndex, Name);
    add_to_output(VectorOutput, &VectorIndex, ";\n");

    // Generate the function calls
    //
    //
    // void Vector_'Type'_init(Vector_'Type' *Vec) {
    //      Vec->Items = malloc(100 * sizeof('Type'));
    //      Vec->TotSize = 100;
    //      Vec->CurSize = 0;
    // }
    add_to_output(VectorOutput, &VectorIndex, "void ");
    add_to_output(VectorOutput, &VectorIndex, Name);
    add_to_output(VectorOutput, &VectorIndex, "_init(");
    add_to_output(VectorOutput, &VectorIndex, Name);
    add_to_output(VectorOutput, &VectorIndex, " *Vec) {\n");
    add_to_output(VectorOutput, &VectorIndex, TAB);
    add_to_output(VectorOutput, &VectorIndex, "Vec->Items = malloc(100 * sizeof(");
    add_to_output(VectorOutput, &VectorIndex, Type);
    add_to_output(VectorOutput, &VectorIndex, "));\n");
    add_to_output(VectorOutput, &VectorIndex, TAB);
    add_to_output(VectorOutput, &VectorIndex, "Vec->TotSize = 100;\n");
    add_to_output(VectorOutput, &VectorIndex, TAB);
    add_to_output(VectorOutput, &VectorIndex, "Vec->CurSize = 0;\n");
    add_to_output(VectorOutput, &VectorIndex, "}\n");

    // void vector_'Type'_expand(vector_'Type' *Vec) {
    //     Vec->TotSize = Vec->TotSize  * 2;
    //     Vec->Items = realloc(Vec->Items, sizeof('Type') * Vec->TotSize);
    // }
    add_to_vector_output("void vector_");
    add_to_vector_output(Type);
    add_to_vector_output("_expand(vector_");
    add_to_vector_output(Type);
    add_to_vector_output(" *Vec) {\n");
    add_to_vector_output(TAB);
    add_to_vector_output("Vec->TotSize = Vec->TotSize * 2;\n");
    add_to_vector_output(TAB);
    add_to_vector_output("Vec->Items = realloc(Vec->Items, sizeof(");
    add_to_vector_output(Type);
    add_to_vector_output(") * Vec->TotSize);\n");
    add_to_vector_output("}\n");

    // void Vector_'Type'_push(Vector_'Type' *Vec, 'Type' Item) {
    //      if (Vec->TotSize == Vec->CurSize) {
    //      }
    //      Vec->Items[Vec->CurSize++] = Item;
    //  }
    add_to_vector_output("void ");
    add_to_vector_output(Name);
    add_to_vector_output("_push(");
    add_to_vector_output(Name);
    add_to_vector_output(" *Vec, ");
    add_to_vector_output(Type);
    add_to_vector_output(" Item) {\n");
    add_to_vector_output(TAB);
    add_to_vector_output("if (Vec->TotSize == Vec->CurSize) {\n");
    add_to_vector_output(TAB);
    add_to_vector_output(TAB);
    add_to_vector_output("vector_");
    add_to_vector_output(Type);
    add_to_vector_output("_expand(Vec);\n");
    add_to_vector_output(TAB);
    add_to_vector_output("}\n");
    add_to_vector_output(TAB);
    add_to_vector_output("Vec->Items[Vec->CurSize++] = Item;\n");
    add_to_vector_output("}\n");

    //void vector_'Type'_insert(vector_'Type' *Vec, 'Type' Pos, 'Type' Item) {
    //    for ('Type' i = Vec->CurSize + 1; i > Pos - 1; i--) {
    //        Vec->Items[i+1] = Vec->Items[i]; 
    //    }
    //    Vec->Items[Pos] = Item;
    //    Vec->CurSize++;
    //}
    add_to_vector_output("void vector_");
    add_to_vector_output(Type);
    add_to_vector_output("_insert(vector_");
    add_to_vector_output(Type);
    add_to_vector_output(" *Vec, int Pos, ");
    add_to_vector_output(Type);
    add_to_vector_output(" Item) {\n");
    add_to_vector_output(TAB);
    add_to_vector_output("if (Vec->TotSize == Vec->CurSize) {\n");
    add_to_vector_output(TAB);
    add_to_vector_output(TAB);
    add_to_vector_output("vector_");
    add_to_vector_output(Type);
    add_to_vector_output("_expand(Vec);\n");
    add_to_vector_output(TAB);
    add_to_vector_output("}\n");
    add_to_vector_output(TAB);
    add_to_vector_output("for (int i = Vec->CurSize + 1; i > Pos - 1; i--) {\n");
    add_to_vector_output(TAB);
    add_to_vector_output(TAB);
    add_to_vector_output("Vec->Items[i+1] = Vec->Items[i];\n");
    add_to_vector_output(TAB);
    add_to_vector_output("}\n");
    add_to_vector_output(TAB);
    add_to_vector_output("Vec->Items[Pos] = Item;\n");
    add_to_vector_output(TAB);
    add_to_vector_output("Vec->CurSize++;\n");
    add_to_vector_output("}\n");
    

    

    //  inline 'Type'* vector_'Type'_at(vector_'Type' Vec, int Pos) {
    //      return &Vec.Items[Pos]
    //  }
    add_to_vector_output("static inline ");
    add_to_vector_output(Type);
    add_to_vector_output("* vector_");
    add_to_vector_output(Type);
    add_to_vector_output("_at(vector_");
    add_to_vector_output(Type);
    add_to_vector_output(" Vec, int Pos) {\n");
    add_to_vector_output(TAB);
    add_to_vector_output("return &Vec.Items[Pos];\n");
    add_to_vector_output("}\n");


    // inline 'Type'* vector_'Type'_front(vector_'Type' Vec) {
    //      return &Vec.Items[0];
    // }
    add_to_vector_output("static inline ");
    add_to_vector_output(Type);
    add_to_vector_output("* vector_");
    add_to_vector_output(Type);
    add_to_vector_output("_front(vector_");
    add_to_vector_output(Type);
    add_to_vector_output(" Vec) {\n");
    add_to_vector_output(TAB);
    add_to_vector_output("return &Vec.Items[0];\n");
    add_to_vector_output("}\n");

    // static inline void vector_'Type'_free(vector_'Type' *Vec) {
    //      free(Vec->Items);
    //      Vec->Items = 0;
    //      Vec->CurSize = 0;
    //      Vec->TotSize = 0;
    // }
    add_to_vector_output("static inline void vector_");
    add_to_vector_output(Type);
    add_to_vector_output("_free(vector_");
    add_to_vector_output(Type);
    add_to_vector_output(" *Vec) {\n");
    add_to_vector_output(TAB);
    add_to_vector_output("free(Vec->Items);\n");
    add_to_vector_output(TAB);
    add_to_vector_output("Vec->Items = 0;\n");
    add_to_vector_output(TAB);
    add_to_vector_output("Vec->CurSize = 0;\n");
    add_to_vector_output(TAB);
    add_to_vector_output("Vec->TotSize = 0;\n");
    add_to_vector_output("}\n");

    // End the redefinition guard
    add_to_vector_output("#endif\n");

    return Name;
}

static bool parse_vector_function() {
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

        char FuncName[100] = { 0 };
        strcat(FuncName, "vector_");
        strcat(FuncName, VarType);
        strcat(FuncName, "_push");

        add_to_normal_output(FuncName);
        add_to_normal_output("(&");
        add_to_normal_output(VarName);
        add_to_normal_output(", ");
        add_to_normal_output(Args.Next->Arg);

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
        char FuncName[100] = { 0 };
        strcat(FuncName, "*vector_");
        strcat(FuncName, VarType);
        strcat(FuncName, "_at");

        add_to_normal_output(FuncName);
        add_to_normal_output("(");
        add_to_normal_output(VarName);
        add_to_normal_output(", ");
        add_to_normal_output(Args.Next->Arg);

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
        char FuncName[100] = { 0 };
        strcat(FuncName, "*vector_");
        strcat(FuncName, VarType);
        strcat(FuncName, "_front");

        add_to_normal_output(FuncName);
        add_to_normal_output("(");
        add_to_normal_output(VarName);

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
        char FuncName[100] = { 0 };
        strcat(FuncName, "vector_");
        strcat(FuncName, VarType);
        strcat(FuncName, "_insert(&");

        add_to_normal_output(FuncName);

        func_call_args* Iterator = &Args;
        while (Iterator->Next != NULL) {
            add_to_normal_output(Iterator->Arg); 
            add_to_normal_output(", ");

            Iterator = Iterator->Next;
        }
        add_to_normal_output(Iterator->Arg);

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
        char FuncName[100] = { 0 };
        strcat(FuncName, "vector_");
        strcat(FuncName, VarType);
        strcat(FuncName, "_free");

        add_to_normal_output(FuncName);
        add_to_normal_output("(&");
        add_to_normal_output(VarName);

        output_remaining_func_line();
        free_func_call_args(Args);
    }
    return true;
}

// Caller Requirements: free returned value
static char* get_vector_file_name() {
    char* VecOutName = (char *)malloc(sizeof(char) * 100);
    strcat(VecOutName, "__vector");
    char Num[10] = { 0 };
    sprintf(Num,"%d",SourceFileCount);
    strcat(VecOutName, Num);
    strcat(VecOutName, ".h");
    return VecOutName;
}
static int CurVecFile = -1;
static bool parse_vector() {
	if (CurVecFile < SourceFileCount) {
        char IncludeStr[100] = { 0 };
        strcat(IncludeStr, "#include \"");
        char* FileName = get_vector_file_name();
        strcat(IncludeStr, FileName);
        free(FileName);
        strcat(IncludeStr, "\"\n");
		CurVecFile++;
		add_to_global_output(IncludeStr);
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
        VecVariables.Name = malloc(strlen(VarName) * sizeof(char));
        strcpy(VecVariables.Name, VarName);

        VecVariables.Type = malloc(strlen(Type) * sizeof(char));
        strcpy(VecVariables.Type, Type);
    } else {
        add_var_to_list(&VecVariables, Type, VarName);
    }

    // Change the variable name declaration
    // vector_'Type' name;
    add_to_normal_output(VecName);
    add_to_normal_output(" ");
    free(VecName);
    add_to_normal_output(VarName);
    add_to_normal_output(";\n");

    // Insert a call to vector_'Type'_init
    add_tabs_to_normal_output();
    add_to_normal_output("vector_");
    add_to_normal_output(Type);
    add_to_normal_output("_init(&");
    add_to_normal_output(VarName);
    add_to_normal_output(");\n");

    return true;
}

static void empty_vec_types() {
    empty_type_list(&VecTypes);
}
