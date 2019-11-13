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
