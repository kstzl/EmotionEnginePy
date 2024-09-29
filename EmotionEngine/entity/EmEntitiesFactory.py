class EmEntityFactory:
    """
    A factory class responsible for registering and creating
    entity instancesdynamically by class name.

    This class maintains a registry of class names and their corresponding class types,
    allowing entities to be instantiated based on their class name.
    """

    def __init__(self) -> None:
        self.classes = {}

    def register_class(self, class_name: str, _class: any):
        """
        Registers a class in the factory by associating a class name with
        its corresponding class type.

        Args:
            class_name (str): The name of the class to register.
            _class (any): The class type to associate with the class name.
        """
        self.classes[class_name] = _class

    def instantiate_class_by_name(self, class_name: str, creation_data: dict):
        """
        Instantiates a class by its registered name using the provided creation data.

        Args:
            class_name (str): The name of the class to instantiate.
            creation_data (dict): A dictionary of parameters to pass to the class constructor.

        Returns:
            any: An instance of the class corresponding to the given class name.
        """
        return self.classes[class_name](creation_data)
