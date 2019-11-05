from typing import TextIO
class Output:
    global_out = ""
    normal_out = ""

    def output_to_file(self, source_file_count: int, cur_file: TextIO) -> None:
        output_file_name = "__" + cur_file.name
        output_file = open(output_file_name, 'w')

        output_file.write(self.global_out)
        output_file.write(self.normal_out)

        output_file.close()

