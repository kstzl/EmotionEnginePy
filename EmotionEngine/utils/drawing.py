import pygame

from EmotionEngine.types.EmVector2 import EmVector2
from typing import Tuple


def draw_text_centered(
    font: pygame.font.Font,
    surface: pygame.surface.Surface,
    text: str,
    color: Tuple[float, float, float],
    position: Tuple[float, float],
):
    text_rendered = font.render(text, True, color)
    xcenter = position.x
    ycenter = position.y
    surface.blit(text_rendered, text_rendered.get_rect(center=(xcenter, ycenter)))
