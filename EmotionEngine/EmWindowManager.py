import pygame

from typing import Tuple


class EmWindowManager:
    def __init__(
        self,
        width: int = 600,
        height: int = 600,
        title: str = "Emotion Engine Application",
    ) -> None:
        self.__width = width
        self.__height = height
        self.__title = title

        self.__screen = pygame.display.set_mode((self.__width, self.__height))

        self.set_caption(self.__title)

    def set_caption(self, new_caption: str):
        pygame.display.set_caption(new_caption)

    def get_width(self) -> int:
        return self.__width

    def get_height(self) -> int:
        return self.__height

    def get_screen_surface(self) -> pygame.Surface:
        return self.__screen

    def fill_screen(self, fill_color: Tuple[int, int, int] = (0, 0, 0)):
        self.get_screen_surface().fill(fill_color)
