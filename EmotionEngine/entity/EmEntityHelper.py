class EmEntityHelper:
    def __init__(self, entities_manager, window_manager) -> None:
        self.__entities_manager = entities_manager
        self.__window_manager = window_manager

    def get_window_width(self) -> int:
        return self.__window_manager.get_width()

    def get_window_height(self) -> int:
        return self.__window_manager.get_height()

    def get_entities_manager(self):
        return self.__entities_manager
