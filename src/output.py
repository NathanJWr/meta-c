from typing import TextIO
class Output:
    global_out = ""
    normal_out = ""
    vector_out = ""

    def output_to_file(self, source_file_count: int, cur_file: TextIO) -> None:
        output_file_name = "__" + cur_file.name
        vector_file_name = "__vector" + str(source_file_count) + ".h"
        output_file = open(output_file_name, 'w')
        vector_file = open(vector_file_name, 'w')

        output_file.write(self.global_out)
        output_file.write(self.normal_out)

        vector_file.write(self.vector_out)

        vector_file.close()
        output_file.close()


