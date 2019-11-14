def generate_vector(self, vec_type: str) -> str:
    name = "vector_" + vec_type
    tab = "    "
    output = ""

    output += "#include <stdlib.h>\n"
    output += "#ifndef VECTOR_" + vec_type + "_\n"
    output += "#define VECTOR_" + vec_type + "_\n"

    # generate the vec struct
    # Typedef struct {
    #     Type* Items;
    #     int TotSize;
    #     int CurSize;
    # } vector_Type;
    output += "typedef struct {\n"
    output += tab + vec_type + "* items;\n"
    output += tab + "int tot_size;\n"
    output += tab + "int cur_size;\n"
    output += "} vector_" + vec_type + ";\n"


    # void Vector_'Type'_init(Vector_'Type' *Vec) {
    #      Vec->Items = malloc(100 * sizeof('Type'));
    #      Vec->TotSize = 100;
    #      Vec->CurSize = 0;
    # }
    output += "static void " + name + "_init(" + name + " *vec) {\n"
    output += tab + "vec->items = "
    output += "(" + vec_type + " *) "
    output +="malloc(100 * sizeof(" + vec_type + "));\n"
    output += tab + "vec->tot_size = 100;\n"
    output += tab + "vec->cur_size = 0;\n"
    output += "}\n"

    # void vector_'Type'_expand(vector_'Type' *Vec) {
    #     Vec->TotSize = Vec->TotSize  * 2;
    #     Vec->Items = realloc(Vec->Items, sizeof('Type') * Vec->TotSize);
    # }
    output += "static void vector_" + vec_type + "_expand(vector_" + vec_type + " *vec) {\n"
    output += tab + "vec->tot_size = vec->tot_size * 2;\n"
    output += tab + "vec->items = (" + vec_type + " *) "
    output += "realloc(vec->items, sizeof(" + vec_type + ") * vec->tot_size);\n"
    output += "}\n"

    # void Vector_'Type'_push(Vector_'Type' *Vec, 'Type' Item) {
    #      if (Vec->TotSize == Vec->CurSize) {
    #      }
    #      Vec->Items[Vec->CurSize++] = Item;
    #  }
    output += "static void " + name + "_push(" + name + " *vec, " + vec_type + " item) {\n"
    output += tab + "if (vec->tot_size == vec->cur_size) {\n"
    output += tab + tab + "vector_" + vec_type + "_expand(vec);\n"
    output += tab + "}\n"
    output += tab + "vec->items[vec->cur_size++] = item;\n"
    output += "}\n"

    # void vector_'Type'_insert(vector_'Type' *Vec, 'Type' Pos, 'Type' Item) {
    #    for ('Type' i = Vec->CurSize + 1; i > Pos - 1; i--) {
    #        Vec->Items[i+1] = Vec->Items[i]; 
    #    }
    #    Vec->Items[Pos] = Item;
    #    Vec->CurSize++;
    # }
    output += "static void vector_" + vec_type + "_insert(vector_" + vec_type + " *vec, int pos, " + vec_type + " item) {\n"
    output += tab + "for (int i = vec->cur_size + 1; i > pos - 1; i--) {\n"
    output += tab + tab + "vec->items[i+1] = vec->items[i];\n"
    output += tab + "}\n"
    output += tab + "vec->items[pos] = item;\n"
    output += tab + "vec->cur_size++;\n"
    output += "}\n"

    #  inline 'Type'* vector_'Type'_at(vector_'Type' Vec, int Pos) {
    #      return &Vec.Items[Pos]
    #  }
    output += "static inline " + vec_type + "* vector_" + vec_type +"_at(vector_" +vec_type + " vec, int pos) {\n"
    output += tab + "return &vec.items[pos];\n"
    output += "}\n"

    # inline 'Type'* vector_'Type'_front(vector_'Type' vec) {
    #       return &vec->items[0]
    # }
    output += "static inline " + vec_type + "* vector_" + vec_type
    output += "_front(vector_" + vec_type + " vec) {\n"
    output += tab + "return &vec.items[0];\n"
    output += "}\n"

    
    # static inline void vector_'Type'_free(vector_'Type' *Vec) {
    #      free(Vec->Items);
    #      Vec->Items = 0;
    #      Vec->CurSize = 0;
    #      Vec->TotSize = 0;
    # }
    output += "static inline void vector_" + vec_type + "_free(vector_" + vec_type + " *vec) {\n"
    output += tab + "free(vec->items);\n"
    output += tab + "vec->items = 0;\n"
    output += tab + "vec->cur_size = 0;\n"
    output += tab + "vec->tot_size = 0;\n"
    output += "}\n"

    output += "#endif // VECTOR_" + vec_type + "_\n"
    return output

def generate_list(self, list_type) -> str:
    name = "list_" + list_type
    tab = "    "
    output = ""

    output += "#include <stdlib.h>\n"
    if self.bounds_checked:
        output += "#include <assert.h>\n"
    output += "#ifndef list_" + list_type + "_\n"
    output += "#define list_" + list_type + "_\n"

    # typedef strcut _node_type {
    #     type item;
    #     struct _node* next
    # } node_type;
    node_name = "node_" + list_type
    output += "typedef struct _" + node_name + " {\n"
    output += tab + list_type + " item;\n"
    output += tab + "struct _" + node_name + "* next;\n"
    output += "} " + node_name + ";\n"

    # typedef struct {
    #     size_t length;
    #     node_name* head;
    #     node_name* tail;
    # } list_type;
    list_name = "list_" + list_type
    output += "typedef struct {\n"
    output += tab + "size_t length;\n"
    output += tab + node_name + "* head;\n"
    output += tab + node_name + "* tail;\n"
    output += "} " + list_name + ";\n"

    # void list_type_init(list_type* list) {
    #     list->head = NULL;
    #     list->tail = NULL;
    #     list->length = 0
    # }
    function_stub = "list_" + list_type
    output += "static void " + function_stub + "_init(" + function_stub + "* list) {\n"
    output += tab + "list->head = NULL;\n"
    output += tab + "list->tail = NULL;\n"
    output += tab + "list->length = 0;\n"
    output += "}\n"

    # void list_type_pushfront(list_type* list, type item) {
    #     node = malloc(sizeof(node));
    #     node.item = item;
    #     if (!list->head) {
    #         list->head = node;
    #         list->tail = node;
    #         list->length++;
    #         return;
    #     }
    #     node->next = list->head;
    #     list->head = node;
    #     list->length++;
    # }
    output += "static void " + function_stub + "_pushfront(" + function_stub + "* list, " + list_type + " item) {\n"
    output += tab + node_name + "* node = malloc(sizeof(" + node_name + "));\n"
    output += tab + "node->item = item;\n"
    output += tab + "if (!list->head) {\n"
    output += tab + tab + "list->head = node;\n"
    output += tab + tab + "list->tail = node;\n"
    output += tab + tab + "list->tail->next = NULL;\n"
    output += tab + tab + "list->length++;\n"
    output += tab + tab + "return;\n"
    output += tab + "}\n"
    output += tab + "node->next = list->head;\n"
    output += tab + "list->head = node;\n"
    output += tab + "list->length++;\n"
    output += "}\n"

    # void list_type_pushback(list_type* list, type item) {
    #     node* = malloc(sizeof(node_type))
    #     node->item = item;
    #     node->next = NULL;
    #     if (!list->head) {
    #         list->head = node;
    #         list->tail = node;
    #         list->length++;
    #         return;
    #     }
    #     last_node = list->tail;
    #     last_node->next = node;
    #     list->tail = node;
    #     list->length++;
    # }
    output += "static void " + function_stub + "_pushback(" + function_stub + "* list, " + list_type + " item) {\n"
    output += tab + node_name + "* node = malloc(sizeof(" + node_name + "));\n"
    output += tab + "node->item = item;\n"
    output += tab + "node->next = NULL;\n"
    output += tab + "if (!list->head) {\n"
    output += tab + tab + "list->head = node;\n"
    output += tab + tab + "list->tail = node;\n"
    output += tab + tab + "list->length++;\n"
    output += tab + tab + "return;\n"
    output += tab + "}\n"
    output += tab + node_name + "* last_node = list->tail;\n"
    output += tab + "last_node->next = node;\n"
    output += tab + "list->tail = node;\n"
    output += tab + "list->length++;\n"
    output += "}\n"

    # type* list_type_front(list_type list) {
    #     return &list.head->item;
    # }
    output += "static inline " + list_type + "* " + function_stub + "_front(" + function_stub + " list) {\n"
    output += tab + "return &list.head->item;\n"
    output += "}\n"

    # void list_type_popfront(list_type* list) {
    #     node_name* node;
    #     if (!list->head) {
    #         return;
    #     }
    #     node = list->head;
    #     list->head = list->head->next
    #     free(node)
    #     list->length--;
    # }
    output += "static void " + function_stub + "_popfront(" + function_stub + "* list) {\n"
    output += tab + node_name + "* node;\n"
    output += tab + "if (!list->head) {\n"
    output += tab + tab + "return;\n"
    output += tab + "}\n"
    output += tab + "node = list->head;\n"
    output += tab + "list->head = list->head->next;\n"
    output += tab + "free(node);\n"
    output += tab + "list->length--;\n"
    output += "}\n"

    # type* list_type_at(list_type* list, size_t index) {
    #     assert (index > list->length);
    #     assert (index >= 0);
    #     node_type* node = list->head;
    #     for (size_t i = 0; i < index; i++)
    #         node = node->next; 
    #     return &node->item; 
    # }
    output += "static " + list_type + "* " + function_stub + "_at(" + function_stub + " list, size_t index) {\n"
    if self.bounds_checked:
        output += tab + "assert(index < list.length);\n"
        output += tab + "assert(index >= 0);\n"
    output += tab + node_name + "* node = list.head;\n"
    output += tab + "for (size_t i = 0; i < index; i++)\n"
    output += tab + tab + "node = node->next;\n"
    output += tab + "return &node->item;\n"
    output += "}\n"

    # void list_type_free(list_type* list) {
    #     node_type node* = list->head;
    #     while (node) {
    #         tmp = node->next;
    #         free(node);
    #         node = tmp;
    #     }
    # }
    output += "static void " + function_stub + "_free(" + function_stub + "* list) {\n"
    output += tab + node_name + "* node = list->head;\n"
    output += tab + "while (node) {\n"
    output += tab + tab + node_name + "* tmp = node->next;\n"
    output += tab + tab + "free(node);\n"
    output += tab + tab + "node = tmp;\n"
    output += tab + "}\n"
    output += "}\n"

    output += "#endif //list_" + list_type + "_\n"

    return output
