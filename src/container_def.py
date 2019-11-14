import container_def_pvt
class ContainerDef:
    bounds_checked: bool

    def __init__(self, bounds_checked):
        self.bounds_checked = bounds_checked
    def generate_vector(self, vec_type: str) -> str:
        return container_def_pvt.generate_vector(self, vec_type)
    def generate_list(self, list_type) -> str:
        return container_def_pvt.generate_list(self, list_type)
