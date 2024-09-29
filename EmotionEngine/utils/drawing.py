import pygame

from typing import Tuple


def draw_text_centered(
    font: pygame.font.Font,
    surface: pygame.Surface,
    text: str,
    color: Tuple[float, float, float],
    position: Tuple[float, float],
):
    """
    Draws centered text on a given surface.

    This function renders the specified text using the provided font and color,
    and blits it onto the given surface at the specified position, centered around
    that position.

    Args:
        font (pygame.font.Font): The font to use for rendering the text.
        surface (pygame.Surface): The surface on which to draw the text.
        text (str): The text string to render.
        color (Tuple[float, float, float]): The RGB color of the text, where each component is
                                             a float in the range [0, 255].
        position (Tuple[float, float]): The (x, y) coordinates around which to center the text.

    Returns:
        None
    """
    text_rendered = font.render(text, True, color)
    xcenter = position.x
    ycenter = position.y
    surface.blit(text_rendered, text_rendered.get_rect(center=(xcenter, ycenter)))
