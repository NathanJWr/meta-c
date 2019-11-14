import c_vector_pvt
import c_container
from output import Output
from c_var import CVarData
from c_token import CToken

from typing import List, Dict
from collections import deque
class CVector:
    output: Output
    variables: Dict[str, CVarData] = dict()
    definitions: List[str] = []
    function_defs: str
    bounds_checked: bool

    def __init__(self, output: Output, bounds_checked: bool):
        self.output = output
        self.definitions.clear()
        self.variables.clear()
        self.function_defs = ""
        self.bounds_checked = bounds_checked
    def write_to_file(self, vec_type) -> None:
        return c_vector_pvt.write_to_file(self, vec_type)
    def purge_variables(self, variables: List[str]) -> None:
        return c_vector_pvt.purge_variables(self, variables)
    def parse(self, tokens: deque) -> str:
        return c_container.parse(self, tokens, "vector")
    def parse_function(self, tokens: deque) -> None:
        return c_vector_pvt.parse_function(self, tokens)
    def get_var_type(self, var_name: str, token: CToken) -> str:
        return c_vector_pvt.get_var_type(self, var_name, token)
    def parse_variable(self, tokens: deque, var_name: str) -> None:
        return c_vector_pvt.parse_variable(self, tokens, var_name)
    def generate_definition(self, vec_type: str) -> str:
        return c_vector_pvt.generate_definition(self, vec_type)