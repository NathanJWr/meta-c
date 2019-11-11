class CVarData:
    c_type: str
    pointer: int

    def __init__(self, c_type: str, pointer: int):
        self.c_type = c_type
        self.pointer = pointer
