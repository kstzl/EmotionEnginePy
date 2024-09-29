from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from EmotionEngine.entity.EmEntitiesManager import EmEntitiesManager
    from EmotionEngine.EmWindowManager import EmWindowManager
    from EmotionEngine.EmKeyboardManager import EmKeyboardManager
    from EmotionEngine.sound.EmSoundsManager import EmSoundsManager
    from EmotionEngine.text.EmFontsManager import EmFontsManager


class EmEntityHelper:
    def __init__(
        self,
        entities_manager: "EmEntitiesManager",
        window_manager: "EmWindowManager",
        keyboard_manager: "EmKeyboardManager",
        sounds_manager: "EmSoundsManager",
        fonts_manager: "EmFontsManager",
    ) -> None:
        self.__entities_manager = entities_manager
        self.__window_manager = window_manager
        self.__keyboard_manager = keyboard_manager
        self.__sounds_manager = sounds_manager
        self.__fonts_manager = fonts_manager

    def get_window_width(self) -> int:
        return self.__window_manager.get_width()

    def get_window_height(self) -> int:
        return self.__window_manager.get_height()

    def retrieve_entities_manager(self) -> "EmEntitiesManager":
        return self.__entities_manager

    def retrieve_keyboard_manager(self) -> "EmKeyboardManager":
        return self.__keyboard_manager

    def retrieve_sounds_manager(self) -> "EmSoundsManager":
        return self.__sounds_manager

    def retrieve_fonts_manager(self) -> "EmFontsManager":
        return self.__fonts_manager
