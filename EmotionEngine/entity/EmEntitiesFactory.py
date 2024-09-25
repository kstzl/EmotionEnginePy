class EmEntityFactory:
    def __init__(self) -> None:
        self.classes = {}

    def register_class(self, class_name: str, _class: any):
        self.classes[class_name] = _class

    def instantiate_class_by_name(self, class_name: str, creation_data: dict):
        return self.classes[class_name](creation_data)
