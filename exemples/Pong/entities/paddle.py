import pygame

from EmotionEngine.entity.EmEntity import EmEntity
from EmotionEngine.collisions.AABB import AABB


class Paddle(EmEntity):
    """
    Represents a paddle in the game, which can be controlled by the player or the AI.

    The Paddle class manages the paddle's position, rendering, and collision detection.
    """

    def __init__(self, creation_data: dict) -> None:
        super().__init__(creation_data)

        self.w = 25
        self.h = 150

        self.paddle_type: str = creation_data["paddle_type"]

    def on_begin_play(self):
        """
        Sets the initial position of the paddle at the start of the game.

        The paddle's position is determined by its type (left or right) and is centered
        vertically in the game window.
        """
        helper = self.retrieve_helper()

        y_center = helper.get_window_height() // 2

        if self.paddle_type == "left":
            self.retrieve_pos().x = 30

        elif self.paddle_type == "right":
            self.retrieve_pos().x = helper.get_window_width() - 30 - self.w

        self.retrieve_pos().y = y_center - self.h // 2

    def on_draw(self, surface: pygame.surface):
        """
        Draws the paddle on the specified surface.

        Args:
            surface (pygame.Surface): The surface on which the paddle will be drawn.
        """
        x = self.retrieve_pos().x
        y = self.retrieve_pos().y

        pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(x, y, self.w, self.h))

    def get_bounding_box(self) -> AABB:
        """
        Returns the axis-aligned bounding box (AABB) for the paddle.

        Returns:
            AABB: The bounding box representing the paddle's dimensions.
        """
        return AABB(0, 0, self.w, self.h)


expose_entity("Paddle", Paddle)
