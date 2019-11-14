import c_vector_pvt
import c_container
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
        return c_vector_pvt(self, vec_type)
    def purge_variables(self, variables: List[str]) -> None:
        return c_vector_pvt(self, variables)
    def parse(self, tokens: deque) -> str:
        return c_container.parse(self, tokens, "vector")
    def parse_function(self, tokens: deque) -> None:
        return c_vector_pvt.parse_function(self, tokens)
