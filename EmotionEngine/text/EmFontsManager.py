import os
import pygame

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from EmotionEngine.EmEngine import EmEngine


class EmFontsManager:
    """
    A manager class for loading and handling font objects within the engine.

    This class provides methods to load fonts from a specified directory as well as
    access system fonts using Pygame's font functionality.
    """

    def __init__(self, engine_ref: "EmEngine") -> None:
        self.__engine_ref = engine_ref

    def load_font(self, font_name: str, font_size: int) -> pygame.font.Font:
        """
        Loads a font file from the game's fonts directory and returns a Pygame Font object.

        Args:
            font_name (str): The name of the font file to load, relative to the game's
            fonts directory.
            font_size (int): The size of the font to create.

        Returns:
            pygame.font.Font: A Pygame Font object representing the loaded font.
        """
        game_fonts_directory = self.__engine_ref.get_fonts_directory()

        return pygame.font.Font(
            os.path.join(game_fonts_directory, font_name), font_size
        )

    def load_sys_font(self, font_name: str, font_size: int) -> pygame.font.Font:
        """
        Loads a system font by name and size using Pygame's system font functionality.

        Args:
            font_name (str): The name of the system font to load.
            font_size (int): The size of the font to create.

        Returns:
            pygame.font.Font: A Pygame Font object representing the loaded system font.
        """
        return pygame.font.SysFont(font_name, font_size)
