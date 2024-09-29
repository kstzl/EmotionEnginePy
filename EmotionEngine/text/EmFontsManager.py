import os
import pygame

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from EmotionEngine.EmEngine import EmEngine


class EmFontsManager:
    def __init__(self, engine_ref: "EmEngine") -> None:
        self.__engine_ref = engine_ref

    def load_font(self, font_name: str, font_size: int) -> pygame.font.Font:
        engine_fonts_directory = self.__engine_ref.get_fonts_directory()

        return pygame.font.Font(
            os.path.join(engine_fonts_directory, font_name), font_size
        )

    def load_sys_font(self, font_name: str, font_size: int) -> pygame.font.Font:
        return pygame.font.SysFont(font_name, font_size)
