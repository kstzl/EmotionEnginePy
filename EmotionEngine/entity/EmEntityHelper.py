from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from EmotionEngine.entity.EmEntitiesManager import EmEntitiesManager
    from EmotionEngine.EmWindowManager import EmWindowManager
    from EmotionEngine.EmKeyboardManager import EmKeyboardManager
    from EmotionEngine.sound.EmSoundsManager import EmSoundsManager
    from EmotionEngine.text.EmFontsManager import EmFontsManager


class EmEntityHelper:
    """
    A helper class for `EmEntity` that provides access to various managers, such as
    entity management, window management, keyboard input, sound, and font resources.

    This class abstracts the interaction with these managers, allowing entities to easily
    retrieve necessary information or services during runtime.
    """

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
        """
        Retrieves the width of the game window.

        Returns:
            int: The width of the window.
        """
        return self.__window_manager.get_width()

    def get_window_height(self) -> int:
        """
        Retrieves the height of the game window.

        Returns:
            int: The height of the window.
        """
        return self.__window_manager.get_height()

    def retrieve_entities_manager(self) -> "EmEntitiesManager":
        """
        Retrieves the entities manager, responsible for managing all entities.

        Returns:
            EmEntitiesManager: The entity manager instance.
        """
        return self.__entities_manager

    def retrieve_keyboard_manager(self) -> "EmKeyboardManager":
        """
        Retrieves the keyboard manager, responsible for handling keyboard inputs.

        Returns:
            EmKeyboardManager: The keyboard manager instance.
        """
        return self.__keyboard_manager

    def retrieve_sounds_manager(self) -> "EmSoundsManager":
        """
        Retrieves the sounds manager, responsible for handling in-game sounds.

        Returns:
            EmSoundsManager: The sounds manager instance.
        """
        return self.__sounds_manager

    def retrieve_fonts_manager(self) -> "EmFontsManager":
        """
        Retrieves the fonts manager, responsible for managing and rendering fonts.

        Returns:
            EmFontsManager: The fonts manager instance.
        """
        return self.__fonts_manager
