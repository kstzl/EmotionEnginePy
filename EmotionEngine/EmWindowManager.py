import pygame

from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from EmotionEngine.EmEngine import EmEngine


class EmWindowManager:
    """
    A class to manage the game window's properties and operations.

    This class handles the creation and management of the game window, including
    its dimensions, title, and the ability to fill the screen with a specific color.
    """

    def __init__(
        self,
        width: int = 600,
        height: int = 600,
        title: str = "Emotion Engine Application",
        engine_ref: "EmEngine" = None,
    ) -> None:
        self.__width = width
        self.__height = height
        self.__title = title

        self.__screen = pygame.display.set_mode((self.__width, self.__height))

        self.__engine_ref = engine_ref
        self.__title = title

        self.update_title()

    def set_title(self, new_title: str):
        """
        Sets the window's caption/title.

        Args:
            new_title (str): The new title for the window.
        """
        self.__title = new_title
        self.update_title()

    def update_title(self):
        """Update window title"""
        assert self.__engine_ref is not None
        pygame.display.set_caption(
            f"{self.__title} {'[PAUSED]' if self.__engine_ref.is_game_paused() else ''}"
        )

    def get_width(self) -> int:
        """
        Returns the width of the window.

        Returns:
            int: The width of the window in pixels.
        """
        return self.__width

    def get_height(self) -> int:
        """
        Returns the height of the window.

        Returns:
            int: The height of the window in pixels.
        """
        return self.__height

    def get_screen_surface(self) -> pygame.Surface:
        """
        Returns the current screen surface for drawing.

        Returns:
            pygame.Surface: The surface on which to draw graphics.
        """
        return self.__screen

    def fill_screen(self, fill_color: Tuple[int, int, int] = (0, 0, 0)):
        """
        Fills the screen with a specified color.

        Args:
            fill_color (Tuple[int, int, int]): A tuple representing the RGB color
                                                 to fill the screen. Default is black (0, 0, 0).
        """
        self.get_screen_surface().fill(fill_color)
